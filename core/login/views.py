from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm
from django.http import JsonResponse
from datetime import datetime
import requests
from django.views.decorators.csrf import csrf_exempt
from .models import Visita
from queue import PriorityQueue



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
def get_priority_visits():
    response = requests.get('https://api-eproc-senac.vercel.app/visits')
    if response.status_code == 200:
        return response.json()
    return []



def recalcular_prioridades(request):
    # Obter as visitas da API
    response = requests.get('https://api-eproc-senac.vercel.app/visits')
    visitas = response.json()

    # Filtrar e ordenar as visitas de acordo com a prioridade
    visitas_prioritarias = sorted(
        [
            visita for visita in visitas
            if visita['mp']['primeiraVisita'] and visita['mp']['nivelFrida'] >= 5 and visita['mp']['status'] == 'Ativa'
        ],
        key=lambda v: (
            datetime.fromisoformat(v['mp']['criadoEm'].replace('Z', '')),
            datetime.fromisoformat(v['mp']['expiraEm'].replace('Z', ''))
        )
    )

    # Formatar as datas e horas para um formato amigável
    for visita in visitas_prioritarias:
        data_visita = datetime.fromisoformat(visita['data'].replace('Z', ''))
        hora_inicio = datetime.fromisoformat(visita['horaInicio'].replace('Z', ''))
        hora_fim = datetime.fromisoformat(visita['horaFim'].replace('Z', ''))

        visita['dataFormatada'] = data_visita.strftime('%d/%m/%Y')
        visita['horaInicioFormatada'] = hora_inicio.strftime('%H:%M')
        visita['horaFimFormatada'] = hora_fim.strftime('%H:%M')

    # Renderizar a lista de visitas prioritárias
    return render(request, 'lista_visitas.html', {'visitas': visitas_prioritarias})
@csrf_exempt
def register_visit(request):
    if request.method == 'POST':
        try:
            numero_processo = request.POST.get('numero-processo')
            data_expiracao = request.POST.get('data-expiracao')
            funcional = request.POST.get('id-funcional')
            data_visita = request.POST.get('data-visita')
            hora_inicio = request.POST.get('hora-inicio')
            hora_final = request.POST.get('hora-final')
            presente = request.POST.get('presente')
            status = request.POST.get('status')

            # Validando campos obrigatórios
            if not numero_processo or not data_visita or not hora_inicio or not hora_final or not status:
                raise ValueError("Todos os campos são obrigatórios.")

            # Convertendo para int
            mp_id = int(numero_processo)
            idfuncional = int(funcional)

            # Convertendo datas e horas para o formato ISO
            data_visita_iso = f"{data_visita}T00:00:00.000Z"
            hora_inicio_iso = f"{data_visita}T{hora_inicio}:00.000Z"
            hora_final_iso = f"{data_visita}T{hora_final}:00.000Z"

            # Convertendo 'presente' para booleano
            presente = True if presente == 'true' else False

            # Dados formatados para o JSON
            data = {
                'mpId': mp_id,
                'policialId': idfuncional,  # Exemplo de ID fixo, mude conforme necessário
                'data': data_visita_iso,
                'horaInicio': hora_inicio_iso,
                'horaFim': hora_final_iso,
                'presente': presente,
                'status': status
            }

            # Envie os dados para a API
            response = requests.post('https://api-eproc-senac.vercel.app/visits', json=data)

            if response.status_code == 201:
                messages.success(request, "Visita Cadastrada com Sucesso.")
                return redirect('register_visit')  # redireciona para uma página de sucesso
            else:
                return JsonResponse(response.json(), status=response.status_code)

        except (ValueError, TypeError) as e:
            messages.error(request, f"Erro ao registrar visita: {str(e)}")
            return redirect('register_visit')  # Redireciona de volta para o formulário em caso de erro

    else:
        # Caso GET, apenas renderiza o formulário
        priority_visits = get_priority_visits()  # Substitua com a função adequada para obter visitas prioritárias
        return render(request, 'register_visit.html', {'priority_visits': priority_visits})

def formatar_data_hora(data_iso):
    # Converter a string ISO 8601 para um objeto datetime
    data = datetime.fromisoformat(data_iso.replace('Z', '+00:00'))
    
    # Formatar a data no formato amigável
    data_formatada = data.strftime('%d/%m/%Y')
    
    return data_formatada

def formatar_hora(hora_iso):
    # Converter a string ISO 8601 para um objeto datetime
    hora = datetime.fromisoformat(hora_iso.replace('Z', '+00:00'))
    
    # Formatar a hora no formato amigável
    hora_formatada = hora.strftime('%H:%M')
    
    return hora_formatada

def lista_visitas(request):
    if request.method == 'POST':
        # Recebendo os dados do formulário
        numero_processo = request.POST.get('numero_processo')
        id_policial = request.POST.get('id_policial')
        data_expiracao = request.POST.get('data_expiracao')

        # Validar os dados (por exemplo, verificar se todos foram preenchidos)
        if not numero_processo or not id_policial or not data_expiracao:
            return JsonResponse({'error': 'Todos os campos são obrigatórios.'}, status=400)

        # Formatar os dados conforme necessário para a API
        data = {
            'mpId': int(numero_processo),  # Assumindo que 'numero_processo' é o 'mpId'
            'policialId': int(id_policial),  # Convertendo para inteiro
            'dataExpiracao': data_expiracao,  # Assumindo que 'data_expiracao' está no formato YYYY-MM-DD
        }

        # Enviar os dados para a API do orquestrador de fila das visitas
        try:
            response = requests.post('https://api-eproc-senac.vercel.app/visits', json=data)
            if response.status_code == 201:
                # Sucesso: recalcular a lista de visitas prioritárias
                return recalcular_prioridades(request)
            else:
                # Retornar mensagem de erro da API
                return JsonResponse(response.json(), status=response.status_code)
        except requests.exceptions.RequestException as e:
            # Tratar erros de requisição (por exemplo, conexão falhou)
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return recalcular_prioridades(request)

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




