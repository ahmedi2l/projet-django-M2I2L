from django import forms
from .models import Recette

from  django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterUserForm(UserCreationForm):
    # email = forms.EmailField(label=u'Courriel', required=True)
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")

'''
#Ancien formulaire de création d'un utilisateur
class RegisterUserForm(forms.Form):
    username = forms.CharField(label=u'Login', max_length=100)
    password = forms.CharField(label=u'Mot de passe', max_length=100, widget=forms.PasswordInput)
    email = forms.EmailField(label=u'Courriel')
'''


class RecetteForm(forms.ModelForm):
    class Meta:
        model = Recette
        # fields = ('title', 'type', 'difficulty', 'cost', 'preparationTime', 'cookTime', 'restTime')
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