from django.urls import path,include
from . import views



urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),
    path('logout', views.log_out, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('menu/', views.menu, name='menu'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart, name='cart'),
    path('team/', views.team, name='team'),
    path('checkout/', views.checkout, name='checkout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update_item/', views.update_item, name='update_item'),
    path('food_detail/<int:pk>', views.food_detail, name='food_detail'),
    path('order_detail/<int:pk>', views.order_detail, name='order_detail'),
    path('reserve/', views.reserve_table, name='reserve'),
    path('add_card', views.add_card, name='add_card'),
    path('add_address', views.add_address, name='add_address'),
    path('cards', views.cards, name='cards'),
    path('address', views.address, name='address'),
    path('delete_card/<int:card_id>/', views.delete_card, name='delete_card'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    

]