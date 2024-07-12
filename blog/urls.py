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
    path('reserve/', views.reserve_table, name='reserve'),

]