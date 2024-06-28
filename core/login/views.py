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





def buscar_cidades(request):
    termo = request.GET.get('termo', '')
    if termo:
        response = requests.get(f'https://servicodados.ibge.gov.br/api/v1/localidades/municipios')
        todas_cidades = response.json()
        cidades_filtradas = [
            {'nome': cidade['nome'], 'estado': cidade['microrregiao']['mesorregiao']['UF']['sigla']}
            for cidade in todas_cidades if termo.lower() in cidade['nome'].lower()
        ]
        return JsonResponse(cidades_filtradas, safe=False)
    return JsonResponse([], safe=False)
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
# No arquivo views.py do seu app Django

def register_person(request):
    if request.method == 'POST':
        # Extrair dados do formulário
        nome = request.POST.get('nome')
        nacionalidade = request.POST.get('nacionalidade-select')
        estado_civil = request.POST.get('estado-civil-select')
        genero = request.POST.get('genero-select')
        cpf = request.POST.get('cpf')
        rg = request.POST.get('rg')
        filiacao_paterna = request.POST.get('filiacao-paterna')
        filiacao_materna = request.POST.get('filiacao-materna')
        data_nascimento = request.POST.get('data-nascimento')
        naturalidade = request.POST.get('naturalidade')
        instrucao = request.POST.get('instrucao')
        profissao = request.POST.get('profissao')
        local_trabalho = request.POST.get('local-trabalho')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        role = request.POST.get('role')

        # Extrair dados do endereço do formulário
        logradouro = request.POST.get('logradouro')
        numero = request.POST.get('numero')
        complemento = request.POST.get('complemento')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')
        cep = request.POST.get('cep')

        campos = request.POST.items()

        for campo, valor in campos:
            if not valor.strip():
                messages.error(request, "Espaços em Brancos")
                return redirect('/register_person')

        # Dados do endereço
        endereco_data = {
            "logradouro": logradouro,
            "numero": numero,
            "complemento": complemento,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "cep": cep
        }

        # Criar endereço no sistema local (supondo que você tenha um modelo Endereco)
        endereco = Endereco.objects.create(**endereco_data)

        # Dados do formulário da pessoa
        form_data = {
            "enderecoId": endereco.id,
            "nome": nome,
            "nacionalidade": nacionalidade,
            "estadoCivil": estado_civil,
            "sexo": genero,
            "cpf": str(cpf),
            "rg": int(rg),
            "telefone": telefone,
            "email": email,
            "profissao": profissao,
            "filiacaoMaterna": filiacao_materna,
            "filiacaoPaterna": filiacao_paterna,
            "dataNascimento": data_nascimento,
            "naturalidade": naturalidade,
            "instrucao": instrucao,
            "localTrabalho": local_trabalho
        }

        api = ('https://api-eproc-senac.vercel.app/aggressors' if role == "agressor" else 'https://api-eproc-senac.vercel.app/victims')

        # Enviando os dados da pessoa para a API
        response = requests.post(api, json=form_data)
        
        if response.status_code == 201:
            messages.success(request, "Cadastrada com Sucesso.")
            return redirect('/register_person')
        else:
            messages.error(request, "Falha Ao Cadastrar!")
            return redirect('/register_person')

    return render(request, 'register_person.html')

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




