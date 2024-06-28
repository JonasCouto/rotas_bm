# login/urls.py
from django.contrib import admin

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="register"),
    path('', views.login, name='login'),  # Certifique-se que 'login_view' é a função correta
    path('/navigation_menu', views.navigation_menu, name='navigation_menu'),
    path('/register_visit', views.register_visit, name='register_visit'),
    path('/lista_visitas', views.lista_visitas, name='lista_visitas'),
]