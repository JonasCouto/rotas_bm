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
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm
from django.http import JsonResponse
from .utils import valida_cpf
import requests

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
    if request.method == 'GET':
        return render(request, "register_protective_measure.html")
    
    elif request.method == 'POST':
        numero_processo = request.POST.get('numero_processo')
        numero_documento = request.POST.get('numero_documento')
        nome_vitima = request.POST.get('nome_vitima')
        nome_agressor = request.POST.get('nome_agressor')
        orgao_expedidor = request.POST.get('orgao_expedidor')
        tipo = request.POST.get('tipo')
        data_registro = request.POST.get('data_registro')
        hora_registro = request.POST.get('hora_registro')
        fato = request.POST.get('fato')
        inicio = request.POST.get('inicio')
        data_expiracao = request.POST.get('data_expiracao')
        form_frida = request.POST.get('form_frida')
        status = request.POST.get('status')

        if len(numero_processo) != 7 or numero_processo.isdigit() == False:
            messages.add_message(request, constants.ERROR, "Número do processo inválido.")
            print(numero_processo.isdigit())
            return redirect('/register_protective_measure')
        
        
        
        messages.add_message(request, constants.SUCCESS, "Registrado com sucesso.")
        return redirect('/register_protective_measure')


# numero_processo, numero_documento, nome_vitima, nome_agressor, 
# orgao_expedidor, tipo, data_registro, 
# hora_registro, fato, inicio, data-expiracao, form-frida, status

def validar_cpf(request):
    if request.method == 'POST':
        cpf_digitado = request.POST.get('cpf', '')
        cpf_valido = valida_cpf(cpf_digitado)

        # Retorna um JSON indicando se o CPF é válido ou não
        return JsonResponse({'cpf_valido': cpf_valido})

    # Lida com requisições GET, se necessário
    return render(request, 'seu_template.html')

def list_protective_measures(request):
    url = 'https://api-eproc-senac.vercel.app/protective-measures'
    
    # Fazendo a requisição GET
    response = requests.get(url)
    
    # Verificando se a requisição foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        medidas_protetivas = response.json()  # Convertendo a resposta para JSON
    else:
        medidas_protetivas = []  # Tratamento para caso de erro
    
    # Renderizando o template com os dados recebidos da API
    return render(request, 'list_protective_measures.html', {'medidas_protetivas': medidas_protetivas})




