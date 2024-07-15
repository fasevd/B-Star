# app/myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.enter_email, name='enter_email'),
    path('enter_code/', views.enter_code, name='enter_code'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
]