# login/urls.py
from django.contrib import admin

from django.urls import path
from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="register"),
    path('', views.login, name='login'),  # Certifique-se que 'login_view' é a função correta
    path('/navigation_menu', views.navigation_menu, name='navigation_menu'),
    path('register_person/', views.register_person, name='register_person'),
    path('buscar_cidades/', views.buscar_cidades, name='buscar_cidades'),
    
    
]