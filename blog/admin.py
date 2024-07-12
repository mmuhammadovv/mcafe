from django.contrib import admin
from .models import  *

# Register your models here.

admin.site.register(Category)
admin.site.register(Food)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Table)
admin.site.register(Booking)
admin.site.register(Contact)
admin.site.register(Team)


