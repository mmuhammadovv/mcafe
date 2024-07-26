from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import *
from django.contrib.auth.models import User , auth
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.views.decorators.http import require_POST, require_http_methods
from django.db import IntegrityError
from .forms import *
from django.utils import timezone
from datetime import datetime
# Create your views here.




def index(request):
    teams = Team.objects.all()

    return render(request, 'index.html', {"teams":teams})



def team(request):
    teams = Team.objects.all()


    return render(request, 'team.html', {'teams':teams})    


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
        order = Order.objects.filter(user=customer, is_payed=False).first()
        items = order.order_item.all() if order else []
        total_price = sum(item.get_total for item in items)
        total_quantity = sum(item.quantity for item in items)
        cards = Card.objects.filter(user=customer)
        address = Address.objects.filter(user=customer)

        if request.method == 'POST':
            user = request.user
            card_id = request.POST.get('card')
            phone_number = request.POST.get('phone_number')
            address_id = request.POST.get('address')
            
            card = get_object_or_404(Card, id=card_id, user=user)
            address = get_object_or_404(Address, id=address_id, user=user)
            
            if order:
                order.card = card
                order.address = address
                order.is_payed = True
                order.phone_number = phone_number
                order.save()
                messages.info(request, 'Оплата сделан наши курьеры скоро свяжутся с вами')
                return redirect('menu')

    else:
        order = {}
        items = []
        total_quantity = 0
        total_price = 0

    context = {
        'items': items,
        'order': order,
        'total_quantity': total_quantity,
        'total_price': total_price,
        'cards': cards,
        'address':address
    }

    return render(request, 'checkout.html', context)



@login_required(login_url='login')
def order_detail(request, pk):

    order = Order.objects.get(pk=pk)
    items = order.order_item.all() 
    total_price = sum(item.get_total for item in items)
    total_quantity = sum(item.quantity for item in items)

    context = {
        'items': items,
        'order': order,
        'total_quantity': total_quantity,
        'total_price': total_price,
    }


    return render(request, 'order_detail.html', context)


@login_required(login_url='login')
def add_address(request):

    if request.method == 'POST':
        user = request.user
        city = request.POST.get('city')
        region = request.POST.get('region')
        apartment = request.POST.get('apartment')
        query = Address(user=user, city=city, region=region, apartment=apartment)
        query.save()
        messages.info(request, 'Адрес успешно добавлен')
        return redirect('address')





    return render(request, 'add_address.html', )


@login_required(login_url='login')
def address(request):

    address = Address.objects.filter(user=request.user)

    return render(request, 'address.html', {'address':address})



@require_http_methods(["DELETE"])
def delete_address(request, address_id):
    address = Address.objects.filter(id=address_id, user=request.user).first()
    if address:
        address.delete()
        return JsonResponse({'message': 'Адрес успешно удален.'}, status=200)


@login_required(login_url='login')
def add_card(request):

    if request.method == 'POST':
        user = request.user
        card_number = request.POST.get('card_number')
        owner_fullname = request.POST.get('owner_fullname')
        cvv = request.POST.get('cvv')
        query = Card(user=user, card_number=card_number, owner_fullname=owner_fullname, cvv=cvv)
        query.save()
        messages.info(request, 'Карта успешно добавлен')
        return redirect('cards')



    return render(request, 'add_card.html')


@login_required(login_url='login')
def cards(request):

    cards = Card.objects.filter(user=request.user)

    context = {
        'cards':cards
    }

    return render(request,  'cards.html', context)


@require_http_methods(["DELETE"])
def delete_card(request, card_id):
    card = Card.objects.filter(id=card_id, user=request.user).first()
    if card:
        card.delete()
        return JsonResponse({'message': 'Карта успешно удалена.'}, status=200)


@login_required(login_url='login')
def dashboard(request):

    orders = Order.objects.filter(user=request.user)
    total_spent = sum(order.get_cart_total for order in orders if order.is_payed)

    context = {
        'orders':orders,
        'total_spent':total_spent,
    }

    return render(request, 'dashboard.html', context)


def logoutfunction(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def reserve_table(request):
    if request.method == 'POST':
        table_id = request.POST.get('table_id')
        booking_start = request.POST.get('booking_start')
        booking_end = request.POST.get('booking_end')
        
        # Convert the input strings to datetime objects and make them timezone-aware
        booking_start = timezone.make_aware(datetime.strptime(booking_start, "%Y-%m-%dT%H:%M"))
        booking_end = timezone.make_aware(datetime.strptime(booking_end, "%Y-%m-%dT%H:%M"))
        
        # Ensure booking start and end are not in the past
        now = timezone.now()
        if booking_start < now or booking_end < now:
            messages.error(request, 'Вы не можете забронировать столик на прошедшее время.')
            return redirect('reserve')

        table = Table.objects.get(id=table_id)

        # Check for overlapping bookings
        overlapping_bookings = Booking.objects.filter(
            table=table,
            booking_start__lt=booking_end,
            booking_end__gt=booking_start
        )
        
        if overlapping_bookings.exists():
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
        'bookings': bookings,
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

