from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Category'    
        verbose_name_plural = 'Categories'


class Food(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()                   
    image = models.ImageField(upload_to='images')
    description = models.TextField()
    ingredients = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(null=True, blank=True)


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Food'
        verbose_name_plural = 'Foods'


    def save(self, *args, **kwargs):
        super(Food, self).save(*args, **kwargs)  


class Table(models.Model):
    number_of_person = models.IntegerField()
    number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"Table {self.number} for {self.number_of_person} persons"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    booking_start = models.DateTimeField()
    booking_end = models.DateTimeField()

    def __str__(self):
        return f"{self.user} booked {self.table} from {self.booking_start} to {self.booking_end}"
    
class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.IntegerField(max_length=16)
    owner_fullname = models.CharField(max_length=255)
    cvv = models.IntegerField(max_length=3)
    
    def __str__(self):
        return str(self.card_number)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    apartment = models.CharField(max_length=255)


    def __str__(self) -> str:
        return self.city


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=16)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    is_payed = models.BooleanField(default=False)
    invoice_id = models.CharField(max_length=50)
    ordered_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)

    @property
    def get_cart_total(self):
        orderitems = self.order_item.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.order_item.all()
        total = sum([item.quantity for item in orderitems])
        return total
    

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    product = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Contact(models.Model):

    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.TextField()
    message = models.TextField()
    
    def __str__(self) -> str:
        return self.name

class Team(models.Model):
    img = models.ImageField(upload_to='team')
    name = models.CharField(max_length=255)
    exprience = models.IntegerField()
    social_nicknam = models.CharField(max_length=50)


    def __str__(self) -> str:
        return self.name