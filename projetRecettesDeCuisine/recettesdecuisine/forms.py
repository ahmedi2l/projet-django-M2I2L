from django import forms
from .models import Recette, Choice

from  django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterUserForm(UserCreationForm):
    # email = forms.EmailField(label=u'Courriel', required=True)
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")

    # Methode permettant de personnaliser les help_texts du formulaire UserCreationForm
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ""
        self.fields['password2'].help_text = ""

class RecetteForm(forms.ModelForm):
    class Meta:
        model = Recette
        fields = ('title', 'type', 'difficultyLevel', 'cost', 'preparationTime',
                  'cookTime', 'restTime', 'images')
        labels = {
            'title': "Titre",
            'difficultyLevel': "Niveau de difficulté",
            'cost': 'Coût',
            'preparationTime ': "Temps de préparation",
            'cookTime': "Temps de cuisson",
            'restTime': "Temps de repos",

        }
        help_texts = {
            'cost': "€",
            'preparationTime': "min.",
            'cookTime': "min",
            'restTime': "min",
        }

class RecipeSearchForm(forms.Form):
    title = forms.CharField(label='Titre', max_length=200, required=False)


class RecipeNoteForm(forms.ModelForm) :
    class Meta:
        model = Choice
        fields = ('recette', 'note',)
