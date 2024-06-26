from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm
from django.http import JsonResponse
from datetime import datetime
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

        try:
            response_vitimas = requests.get('https://api-eproc-senac.vercel.app/victims')
            response_agressores = requests.get('https://api-eproc-senac.vercel.app/agressors')

            if response_vitimas.status_code == 200 and response_agressores.status_code == 200:
                vitimas = response_vitimas.json()
                agressores = response_agressores.json()
            else:
                vitimas = []
                agressores = []
                messages.add_message(request, messages.ERROR, 'Não foi possível obter os nomes de vítimas e agressores.')
        
        except requests.exceptions.RequestException as e:
            vitimas = []
            agressores = []
            messages.add_message(request, messages.ERROR, f'Erro ao conectar com a API: {e}')

        return render(request, "register_protective_measure.html", {'vitimas': vitimas, 'agressores': agressores})
    
    elif request.method == 'POST':

        numero_processo = request.POST.get('numero_processo').strip()
        numero_ocorrencia = request.POST.get('numero_ocorrencia').strip()
        nome_vitima = request.POST.get('nome_vitima').strip()
        nome_agressor = request.POST.get('nome_agressor').strip()
        orgao_expedidor = request.POST.get('orgao_expedidor').strip()
        tipo = request.POST.get('tipo').strip()
        data_registro = request.POST.get('data_registro').strip()
        hora_registro = request.POST.get('hora_registro').strip()
        horario_expiracao = request.POST.get('horario_expiracao').strip()
        data_expiracao = request.POST.get('data_expiracao').strip()
        form_frida = request.POST.get('form_frida')
        status = request.POST.get('status')

        campos = request.POST.items()
        print(status)

        for campo, valor in campos:
            if not valor.strip():
                messages.add_message(request, constants.ERROR, 'Algum campo está vazio ou em branco.')
                return redirect('/register_protective_measure')

        if numero_processo.isdigit() == False:
            messages.add_message(request, constants.ERROR, "Número do processo deve ser apenas números.")
            return redirect('/register_protective_measure')
        
        if numero_ocorrencia.isdigit() == False:
            messages.add_message(request, constants.ERROR, "Número da ocorrência deve ser apenas números.")
            return redirect('/register_protective_measure')
       
        data_registro_iso = f"{data_registro}T{hora_registro}:00.000Z"
        data_expiracao_iso = f"{data_expiracao}T{horario_expiracao}:00.000Z"

        data = {
            'vitimaId': int(nome_vitima),
            'agressorId': int(nome_agressor),
            'tipoAcao': tipo,  
            'numProcesso': int(numero_processo),  
            'numOcorrencia': int(numero_ocorrencia),
            'orgaoExpedidor': orgao_expedidor,
            'primeiraVisita': False,
            'nivelFrida': int(form_frida),
            'status': status,
            'criadoEm': data_registro_iso,
            'expiraEm': data_expiracao_iso
        }

        response = requests.post('https://api-eproc-senac.vercel.app/protective-measures', json=data)       

        if response.status_code == 201:
            messages.add_message(request, constants.SUCCESS, "Registrado com sucesso.")
            return redirect('/register_protective_measure')
    
        else:
            return JsonResponse(response.json(), status=response.status_code)


def list_protective_measures(request):
    url = 'https://api-eproc-senac.vercel.app/protective-measures'
    
    # Fazendo a requisição GET
    response = requests.get(url)
    
    if response.status_code == 200:
        medidas_protetivas = response.json()  
    else:
        medidas_protetivas = []  
    
    return render(request, 'list_protective_measures.html', {'medidas_protetivas': medidas_protetivas})




