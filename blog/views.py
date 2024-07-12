from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import *
from django.contrib.auth.models import User , auth
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from .forms import *
from django.utils import timezone
# Create your views here.




def index(request):
    return render(request, 'index.html')



def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Пароли не совпадают.')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует.')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует.')
            return redirect('signup')

        data = User.objects.create_user(username=username, email=email, password=password1)
        data.save()
        messages.success(request, 'Регистрация прошла успешно.')
        return redirect('login')

    return render(request, 'signup.html')

def about(request):

    return render(request, 'about.html')


def login(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('home')
        
    return render(request, 'login.html')

def log_out(request):
    logout(request)
    messages.success(request, ('You Were log out'))
    return redirect('home')


def contact(request):
    return render(request, 'contact.html')


def menu(request):
    category = Category.objects.all()
    foods = Food.objects.all()

    active_category = request.GET.get('category', '')

    if active_category:
        foods = foods.filter(category=active_category)

    context = {
        'category':category,
        'foods':foods, 
        'active_category':active_category
    }
    return render(request, 'menu.html', context)

def food_detail(request, pk):

    food = Food.objects.get(pk=pk)

    context = {
        'food':food
    }

    return render(request, 'food_detail.html', context)

@login_required(login_url='login')

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order = Order.objects.filter(user=customer, is_payed=False)
        items = [item for o in order for item in o.order_item.all()] 
        total_price = sum(item.get_total for item in items)
        total_quantity = sum(item.quantity for item in items)
    else:
        order = {}
        items = []
        total_quantity = 0
        total_price = 0


    context = {
        'items': items,
        'order':order,
        'total_quantity': total_quantity,
        'total_price': total_price,
    }

    return render(request, 'cart.html', context)


@login_required(login_url='login')

@csrf_exempt
@require_POST
def update_item(request):
    try:
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        print('Action:', action)
        print('ProductId:', productId)

        customer = request.user
        product = Food.objects.get(id=productId)
        order, created = Order.objects.get_or_create(user=customer, is_payed=False)

        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if created:
            orderItem.quantity = 0  # Initialize quantity to 0 if the item is newly created

        if action == 'add':
            orderItem.quantity += 1
        elif action == 'remove':
            orderItem.quantity -= 1

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

        return JsonResponse({'message': 'Item was updated'}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Food.DoesNotExist:
        return JsonResponse({'error': 'Product does not exist'}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)}, status=400)


@login_required(login_url='login')

def checkout(request):

    if request.user.is_authenticated:
        customer = request.user
        order = Order.objects.filter(user=customer, is_payed=False)
        items = [item for o in order for item in o.order_item.all()] 
        total_price = sum(item.get_total for item in items)
        total_quantity = sum(item.quantity for item in items)
        if request.method == 'POST':
            user = request.user
            card = request.POST.get('card')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')  
            
            order = Order.objects.filter(user=user, is_payed=False,).first()
            if order:
                order.card = card
                order.address = address
                order.is_payed = True
                order.phone_number = phone_number
                order.save()
                messages.info(request, 'Оплата сделан наши куреры скоро свяжутся с вами')
                return redirect('menu')

    else:
        order = {}
        items = []
        total_quantity = 0
        total_price = 0



    context = {
        'items': items,
        'order':order,
        'total_quantity': total_quantity,
        'total_price': total_price,
    }

    return render(request, 'checkout.html', context)



@login_required(login_url='login')

def dashboard(request):

    orders = Order.objects.filter(user=request.user)
    total_spent = sum(order.get_cart_total for order in orders if order.is_payed)

    context = {
        'orders':orders,
        'total_spent':total_spent,
    }

    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def reserve_table(request):
    if request.method == 'POST':
        table_id = request.POST.get('table_id')
        booking_start = request.POST.get('booking_start')
        booking_end = request.POST.get('booking_end')
        table = Table.objects.get(id=table_id)

        existing_bookings = Booking.objects.filter(
            table=table,
            booking_start__lt=booking_end,
            booking_end__gt=booking_start
        )

        if existing_bookings.exists():
            messages.error(request, 'Этот столик уже забронирован на выбранное время.')
        else:
            booking = Booking(
                user=request.user,
                table=table,
                booking_start=booking_start,
                booking_end=booking_end
            )
            booking.save()
            messages.success(request, 'Столик успешно забронирован.')
            return redirect('reserve')

    tables = Table.objects.all()
    now = timezone.now()
    for table in tables:
        table.is_booked = Booking.objects.filter(
            table=table,
            booking_start__lt=now,
            booking_end__gt=now
        ).exists()
    
    bookings = Booking.objects.all()
    context = {
        'tables': tables,
        'bookings':bookings,
    }
    return render(request, 'reserve_table.html', context)



def contact(request):
    if request.method=='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')   
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        myquery = Contact(name=name, subject=subject, email=email, message=message)
        myquery.save()
        messages.info(request, 'Мы скоро ответим вам ! ')
        return redirect('/')
    
    return render(request, 'contact.html')

