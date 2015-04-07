from django import forms
from django.forms import ModelForm
from .models import Recette


class LoginForm(forms.Form):
    username = forms.CharField(label='Login', max_length=100)
    password = forms.CharField(label='Mot de passe', max_length=100, widget=forms.PasswordInput)


class RecetteForm(ModelForm):
    class Meta:
        model = Recette
        fields = ['title', 'type']
