from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Home'),
    path('delete/<city_name>/', views.delete_city, name='delete_city'),
    path('about/', views.about, name='About'),
    path('contact/', views.contact, name='Contact'),
]