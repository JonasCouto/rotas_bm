from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

# def login(request):
#     return render(request, "login.html")

from django.shortcuts import render

# Create your views here.


# def index(request):
#     return render(request, "index.html")


# def login(request):
#     return render(request, "login.html")


# core/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm

#Jonas - Metodo do Header
def index(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, "Cadastro realizado com sucesso! Faça o login.")
            return redirect("login")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = UserRegistrationForm()
    return render(request, "index.html", {"form": form})

#Jonas - Metodo do Login
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(
                "navigation_menu"
            )  # Substitua 'protected_page' pelo nome da sua URL protegida
        else:
            messages.error(request, "Nome de usuário ou senha inválidos.")
    return render(request, "login.html")

#Cleiton- Metodo do Painel de Navegação
def navigation_menu(request):
    return render(request, "navigation_menu.html")

#Lucas - Metodo do mapas
def map_direction(request):
    return render(request, "map_direction.html")

#Lucas - Metodo de Cadastrar Pessoa
def register_person(request):
    return render(request, "register_person.html")

#Jonathn - Metodo de Registrar Visita
def register_visit(request):
    return render(request, "register_visit.html")

def register_protective_measure(request):
    return render(request, "register_protective_measure.html")