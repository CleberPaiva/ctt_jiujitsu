# core/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),  # Página inicial
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastrar-aluno/', views.cadastrar_aluno, name='cadastrar_aluno'),  # URL para o cadastro de alunos
    path('criar_mural/', views.criar_mural, name='criar_mural'),  # URL para o cadastro de mural
    path('selecionar-treino/', views.registrar_presenca, name='selecionar_treino'),
    path('registrar-presenca/', views.registrar_presenca, name='registrar_presenca'),
    path('links/', views.links, name='links'),
    path('carteira/', views.carteira, name='carteira'),
    path('digital-card/', views.digital_card, name='digital_card'),
    path('listar-alunos/', views.listar_alunos, name='listar_alunos'),
    path('listar-presencas/', views.listar_presencas, name='listar_presencas'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Adiciona a configuração para servir arquivos de mídia
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

