# core/forms.py
from django import forms
from .models import Aluno
from .models import Mural, Presenca


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'data_nascimento', 'cpf', 'celular', 'email', 'graduacao', 'regional', 'funcao']


class MuralForm(forms.ModelForm):
    class Meta:
        model = Mural
        fields = ['texto_mural']  # Apenas o campo de texto é exibido no formulário


class PresencaForm(forms.ModelForm):
    class Meta:
        model = Presenca
        fields = ['presente']

    aluno = forms.ModelChoiceField(queryset=Aluno.objects.all(), widget=forms.HiddenInput())
