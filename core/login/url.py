# login/urls.py
from django.contrib import admin

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="register"),
    path('', views.login, name='login'),  # Certifique-se que 'login_view' é a função correta
]