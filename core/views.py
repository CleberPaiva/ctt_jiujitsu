from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AlunoForm
from .models import Treino, Aluno, Professor, Presenca
from .models import Mural
from .forms import MuralForm
from .forms import PresencaForm
from django.utils import timezone


DAYS_TRANSLATION = {
    'Monday': 'Segunda',
    'Tuesday': 'Terça',
    'Wednesday': 'Quarta',
    'Thursday': 'Quinta',
    'Friday': 'Sexta',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}


@login_required
def home(request):
    # Verifica se o usuário logado é um professor
    eh_professor = Professor.objects.filter(email=request.user.email).exists()

    treino = None
    treinos = None
    regional_usuario = None

    recados = Mural.objects.all().order_by('-data_de_criacao')

    if request.user.is_authenticated:
        try:
            # Tenta encontrar o usuário como Aluno
            aluno = Aluno.objects.get(email=request.user.email)
            treino = aluno.treino  # Obtém o treino específico associado ao Aluno
            regional_usuario = aluno.regional
        except Aluno.DoesNotExist:
            try:
                # Se não é Aluno, tenta encontrar o usuário como Professor
                professor = Professor.objects.get(email=request.user.email)
                regional_usuario = professor.regional
                # Obtém todos os treinos da mesma regional do Professor
                treinos = Treino.objects.filter(regional=regional_usuario)
                
                # Adiciona a lista de alunos diretamente em cada treino
                for treino_item in treinos:
                    treino_item.alunos = Aluno.objects.filter(treino=treino_item, regional=regional_usuario).order_by('nome')
            except Professor.DoesNotExist:
                pass

    # Renderiza a página com o treino específico do aluno ou todos os treinos e alunos para a regional do professor
    return render(request, 'core/home.html', {
        'treino': treino,  # Treino específico do aluno
        'treinos': treinos,  # Todos os treinos para a regional do professor
        'regional': regional_usuario,
        'recados': recados,
        'eh_professor': eh_professor
    })


@login_required
def cadastrar_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redireciona para a página inicial ou para outra página de sucesso
    else:
        form = AlunoForm()
    return render(request, 'core/cadastrar_aluno.html', {'form': form})


@login_required
def criar_mural(request):
    if request.method == 'POST':
        form = MuralForm(request.POST)
        if form.is_valid():
            mural = form.save(commit=False)
            mural.usuario_responsavel = request.user  # Define o usuário logado como responsável
            mural.save()
            return redirect('home')  # Redireciona para a página do mural (substitua com a URL apropriada)
    else:
        form = MuralForm()
    return render(request, 'core/criar_mural.html', {'form': form})

@login_required
def registrar_presenca(request):
    try:
        professor = Professor.objects.get(email=request.user.email)
    except Professor.DoesNotExist:
        return redirect('home')

    # Obter o dia da semana atual (exemplo: 'Terça')
    dia_semana_en = timezone.now().strftime('%A')
    dia_semana = DAYS_TRANSLATION.get(dia_semana_en, dia_semana_en)

    # Imprimir o dia da semana no console para depuração
    #print(f"Dia da semana atual: {dia_semana}")

    # Filtrar treinos disponíveis para a regional do professor e verificar o dia da semana
    treinos_disponiveis = Treino.objects.filter(
        regional=professor.regional
    ).filter(dia_semana__icontains=dia_semana)

    if not treinos_disponiveis:
        # Se não há treinos para hoje
        mensagem = "Não há treinos disponíveis para hoje na sua regional."
        return render(request, 'core/selecionar_treino.html', {'treinos_disponiveis': treinos_disponiveis, 'mensagem': mensagem})

    if request.method == 'POST' and 'treino_id' in request.POST:
       
        # Verifica o conteúdo de request.POST
        print("Conteúdo de request.POST:", request.POST)

        treino_id = request.POST.get('treino_id')
        treino = get_object_or_404(Treino, id=treino_id)
        alunos = Aluno.objects.filter(treino=treino)

        # Verificação de depuração para confirmar o treino selecionado
        #print(f"Treino selecionado para salvamento: {treino}")

        if 'save' in request.POST:
            # Verifica o conteúdo de request.POST
            print("Conteúdo de request.POST:", request.POST)

            for aluno in alunos:
                presente = request.POST.get(f'presente_{aluno.id}') == 'on'
                Presenca.objects.update_or_create(
                    aluno=aluno,
                    treino=treino,
                    data=timezone.now().date(),
                    defaults={'presente': presente}
                )
                print(f"Presença selecionada para salvamento: {presente}")
            return redirect('home')

        presenca_forms = [(aluno, PresencaForm(initial={'aluno': aluno})) for aluno in alunos]
        return render(request, 'core/registrar_presenca.html', {'treino': treino, 'presenca_forms': presenca_forms})

    return render(request, 'core/selecionar_treino.html', {'treinos_disponiveis': treinos_disponiveis})


@login_required
def links(request):
    return render(request, 'core/links.html')


@login_required
def carteira(request):
    return render(request, 'core/carteira.html')


@login_required
def digital_card(request):
    # Verifica se o usuário logado é um aluno ou professor
    try:
        perfil = Aluno.objects.get(email=request.user.email)
    except Aluno.DoesNotExist:
        perfil = get_object_or_404(Professor, email=request.user.email)

    # Renderiza o cartão com as informações do usuário
    return render(request, 'core/digital_card.html', {'perfil': perfil})


@login_required
def listar_alunos(request):
    try:
        # Verifica se o usuário é um professor
        professor = Professor.objects.get(email=request.user.email)
    except Professor.DoesNotExist:
        return redirect('home')  # Redireciona se não for professor

    # Obtém todos os alunos para exibir na página
    alunos = Aluno.objects.all()
    return render(request, 'core/listar_alunos.html', {'alunos': alunos})


@login_required
def sua_view(request):
    eh_professor = Professor.objects.filter(email=request.user.email).exists()  # Verifica se o usuário é professor
    return render(request, 'home.html', {'eh_professor': eh_professor})


@login_required
def listar_presencas(request):
    # Busca todas as presenças, ordenadas por data
    presencas = Presenca.objects.select_related('aluno', 'treino').order_by('-data')
    return render(request, 'core/listar_presencas.html', {'presencas': presencas})