from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField  # Importa o MultiSelectField
from django.utils import timezone


# Choices para Regional
REGIONAL_CHOICES = [
    ('Regional 1', 'Regional 1'),
    ('Regional 2', 'Regional 2'),
    ('Regional 3', 'Regional 3'),
    ('Regional 4', 'Regional 4'),
    ('Regional 5', 'Regional 5'),
    ('Regional 6', 'Regional 6'),
    ('Regional 7', 'Regional 7'),
    ('Regional 8', 'Regional 8')
]

# Choices para Função
FUNCAO_CHOICES = [
    ('Policial Penal', 'Policial Penal'),
    ('Agente de Segurança Socioeducativo', 'Agente de Segurança Socioeducativo'),
    ('Vigilante', 'Vigilante'),
    ('Técnico', 'Técnico'),
    ('Outros', 'Outros')
]

# Choices para Graduação
GRADUACAO_CHOICES = [
    ('Branco', 'Branco'),
    ('Branco - 1 grau', 'Branco - 1 grau'),
    ('Branco - 2 graus', 'Branco - 2 graus'),
    ('Branco - 3 graus', 'Branco - 3 graus'),
    ('Branco - 4 graus', 'Branco - 4 graus'),
    ('Azul', 'Azul'),
    ('Azul - 1 grau', 'Azul - 1 grau'),
    ('Azul - 2 graus', 'Azul - 2 graus'),
    ('Azul - 3 graus', 'Azul - 3 graus'),
    ('Azul - 4 graus', 'Azul - 4 graus'),
    ('Roxa', 'Roxa'),
    ('Roxa - 1 grau', 'Roxa - 1 grau'),
    ('Roxa - 2 graus', 'Roxa - 2 graus'),
    ('Roxa - 3 graus', 'Roxa - 3 graus'),
    ('Roxa - 4 graus', 'Roxa - 4 graus'),
    ('Marrom', 'Marrom'),
    ('Marrom - 1 grau', 'Marrom - 1 grau'),
    ('Marrom - 2 graus', 'Marrom - 2 graus'),
    ('Marrom - 3 graus', 'Marrom - 3 graus'),
    ('Marrom - 4 graus', 'Marrom - 4 graus'),
    ('Preto', 'Preto'),
    ('Preto - 1 grau', 'Preto - 1 grau'),
    ('Preto - 2 graus', 'Preto - 2 graus'),
    ('Preto - 3 grau', 'Preto - 3 graus'),
    ('Preto - 4 grau', 'Preto - 4 graus'),
    ('Preto - 5 grau', 'Preto - 5 graus'),
    ('Preto - 6 grau', 'Preto - 6 graus')
]

# Choices para Dia da Semana
DIA_SEMANA_CHOICES = [
    ('Segunda', 'Segunda'),
    ('Terça', 'Terça'),
    ('Quarta', 'Quarta'),
    ('Quinta', 'Quinta'),
    ('Sexta', 'Sexta'),
    ('Sábado', 'Sábado'),
    ('Domingo', 'Domingo')
]

# Choices para Horário
HORARIO_CHOICES = [
    (f'{h:02d}:{m:02d}', f'{h:02d}:{m:02d}')
    for h in range(7, 23)  # de 7:00 a 22:00
    for m in (0, 30)       # minutos: 00 e 30
]

class Treino(models.Model):
    regional = models.CharField(max_length=20, choices=REGIONAL_CHOICES)
    dia_semana = MultiSelectField(choices=DIA_SEMANA_CHOICES, max_length=50)  # Permite múltiplos dias
    horario = models.CharField(max_length=5, choices=HORARIO_CHOICES)

    def __str__(self):
        return f"{self.regional} - {' e '.join(self.dia_semana)} às {self.horario}"

# Modelos para Aluno e Professor
class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=11, unique=True)  # CPF usado como username
    celular = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    matricula = models.CharField(max_length=20, unique=True) 
    graduacao = models.CharField(max_length=20, choices=GRADUACAO_CHOICES)
    regional = models.CharField(max_length=20, choices=REGIONAL_CHOICES)
    funcao = models.CharField(max_length=50, choices=FUNCAO_CHOICES)
    treino = models.ForeignKey(Treino, on_delete=models.SET_NULL, null=True, blank=True)
    imagem = models.ImageField(upload_to='alunos_imagens/', null=True, blank=True)
    faixa = models.CharField(max_length=20, choices=GRADUACAO_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        # Verifica se o usuário já existe para esse CPF
        if not User.objects.filter(username=self.cpf).exists():
            # Cria o usuário com o CPF como nome de usuário
            user = User.objects.create_user(
                username=self.cpf,       # Usa o CPF como nome de usuário
                email=self.email,
                password='acaps123'      # Define uma senha padrão que deve ser alterada
            )
            user.first_name = self.nome.split()[0]  # Define o primeiro nome
            user.last_name = ' '.join(self.nome.split()[1:])  # Define o sobrenome, se houver
            user.save()
        super().save(*args, **kwargs)

class Professor(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=11, unique=True)  # CPF usado como username
    celular = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    graduacao = models.CharField(max_length=20, choices=GRADUACAO_CHOICES)
    regional = models.CharField(max_length=20, choices=REGIONAL_CHOICES)
    funcao = models.CharField(max_length=50, choices=FUNCAO_CHOICES)
    imagem = models.ImageField(upload_to='alunos_imagens/', null=True, blank=True)
    faixa = models.CharField(max_length=20, choices=GRADUACAO_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        # Verifica se o usuário já existe para esse CPF
        if not User.objects.filter(username=self.cpf).exists():
            # Cria o usuário com o CPF como nome de usuário
            user = User.objects.create_user(
                username=self.cpf,       # Usa o CPF como nome de usuário
                email=self.email,
                password='acaps123'      # Define uma senha padrão que deve ser alterada
            )
            user.first_name = self.nome.split()[0]  # Define o primeiro nome
            user.last_name = ' '.join(self.nome.split()[1:])  # Define o sobrenome, se houver
            user.save()
        super().save(*args, **kwargs)


class Mural(models.Model):
    data_de_criacao = models.DateTimeField(auto_now_add=True)
    usuario_responsavel = models.ForeignKey(User, on_delete=models.CASCADE)
    texto_mural = models.TextField()

    def __str__(self):
        return f"{self.usuario_responsavel.username} - {self.data_de_criacao.strftime('%d/%m/%Y %H:%M')}"     
    

class Presenca(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE)
    data = models.DateField(default=timezone.now)
    presente = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.aluno.nome} - {self.treino} - {'Presente' if self.presente else 'Faltante'}"