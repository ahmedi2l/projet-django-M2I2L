from django import forms
from django.forms import ModelForm
from .models import Recette


class CreateUserForm(forms.Form):
    username = forms.CharField(label=u'Login', max_length=100)
    password = forms.CharField(label=u'Mot de passe', max_length=100, widget=forms.PasswordInput)
    email = forms.EmailField(label=u'Courriel')


class RecetteForm(forms.ModelForm):
    class Meta:
        model = Recette
        #fields = ('title', 'type', 'difficulty', 'cost', 'preparationTime', 'cookTime', 'restTime')
        labels = {
            'title': "Titre",
            'difficulty': "Difficulté",
            'cost': 'Coût',
            'preparationTime ': "Temps de préparation",
            'cookTime': "Temps de cuisson",
            'restTime': "Temps de repos",

        }
        help_texts = {
            'difficulty': "Niveau de difficulté de la recette",
            'cost': "€",
            'preparationTime': "min.",
            'cookTime': "min",
            'restTime': "min",
        }