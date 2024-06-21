"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login import views
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('login.urls')),
    path("user/", views.index, name="register"),  # Inclua as URLs do aplicativo 'login'
    path('',views.login_view, name='login'),  # Inclua as URLs do aplicativo 'login'
    path('navigation_menu/', views.navigation_menu, name='navigation_menu'), # Panel settings
    path('register_person/', views.register_person, name='register_person'), # Register person
    path('register_visit/', views.register_visit, name='register_visit'), # Register visit      
    path('map_direction/', views.map_direction, name='map_direction'), # Maps
    path('login/', include('login.url')),
    
]
