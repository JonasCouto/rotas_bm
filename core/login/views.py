
# core/views.py
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
@login_required(login_url='/login/')
def navigation_menu(request):
    return render(request, "navigation_menu.html")

# #Jonas
# def logout_view(request):
#     logout(request)
#     return redirect('login')  # redireciona para a página de login após o logout

#Lucas - Metodo do mapas
@login_required(login_url='/login/')
def map_direction(request):
    return render(request, "map_direction.html")


#Lucas - Metodo de Cadastrar Pessoa
@login_required(login_url='/login/')
def register_person(request):
    return render(request, "register_person.html")


#Jonathn - Metodo de Registrar Visita
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

def formatar_data(data_iso):
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
    visitas_info = []
    num_processo = request.POST.get('numProcesso') if request.method == 'POST' else None

    try:
        response = requests.get('https://api-eproc-senac.vercel.app/protective-measures')
        data = response.json()

        for item in data:
            mp_id = item.get('id')
            visitas = item.get('visitas', [])
            processo_numero = item.get('numProcesso')

            for visita in visitas:
                visita_info = {
                    'mp_id': mp_id,
                    'visita_id': visita.get('id'),
                    'data': formatar_data(visita.get('data')),
                    'horaInicio': formatar_hora(visita.get('horaInicio')),
                    'horaFim': formatar_hora(visita.get('horaFim')),
                    'status': visita.get('status'),
                    'presente': visita.get('presente'),
                    'numProcesso': processo_numero,
                }

                if num_processo:
                    if str(processo_numero) == num_processo:
                        visitas_info.append(visita_info)
                else:
                    visitas_info.append(visita_info)

        return render(request, 'lista_visitas.html', {'visitas': visitas_info, 'numProcesso': num_processo})

    except KeyError as e:
        return JsonResponse({'error': f'KeyError: {e}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_protective_measures(request):
    url = 'https://api-eproc-senac.vercel.app/protective-measures'
    response = requests.get(url)

    if response.status_code == 200:
        protective_measures = response.json()
        
        # Contar as visitas por medida protetiva (mpId)
        visits_count = defaultdict(int)
        for measure in protective_measures:
            mp_id = measure['id']
            visits_count[mp_id] = len(measure['visitas'])

        visits_count_dict = dict(visits_count)
        
        return render(request, 'visits_count.html', {'visits_count': visits_count_dict})
    else:
        return render(request, 'error.html', {'error_message': 'Falha ao obter dados da API de medidas protetivas'})

#Raul
@login_required(login_url='/login/')
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

# numero_processo, numero_documento, nome_vitima, nome_agressor, 
# orgao_expedidor, tipo, data_registro, 
# hora_registro, fato, inicio, data-expiracao, form-frida, status
#raul
@login_required(login_url='/login/')
def validar_cpf(request):
    if request.method == 'POST':
        cpf_digitado = request.POST.get('cpf', '')
        cpf_valido = valida_cpf(cpf_digitado)
        response = requests.post('https://api-eproc-senac.vercel.app/protective-measures', json=data)       

        if response.status_code == 201:
            messages.add_message(request, constants.SUCCESS, "Registrado com sucesso.")
            return redirect('/register_protective_measure')
    
        else:
            return JsonResponse(response.json(), status=response.status_code)


#Raul
@login_required(login_url='/login/')
def list_protective_measures(request):
    url = 'https://api-eproc-senac.vercel.app/protective-measures'
    
    # Fazendo a requisição GET
    response = requests.get(url)
    
    if response.status_code == 200:
        medidas_protetivas = response.json()  
    else:
        medidas_protetivas = []  
    
    # Renderizando o template com os dados recebidos da API
    return render(request, 'list_protective_measures.html', {'medidas_protetivas': medidas_protetivas})
    return render(request, 'list_protective_measures.html', {'medidas_protetivas': medidas_protetivas})




