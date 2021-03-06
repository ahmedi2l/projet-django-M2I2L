# -*- coding:utf-8 -*-
from django import forms
from .models import Recette, Choice, Ingredient, PreparationSteps

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
                  'cookTime', 'restTime', 'images', 'preparationSteps', 'ingredientsList')
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
    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(), label=u"Ingrédients",
                                                 required=False, widget=forms.widgets.CheckboxSelectMultiple)
    OPERATOR_CHOICES = (
        ('or', u'Ou'),
        ('and', u'Et')
    )
    operator = forms.ChoiceField(choices=OPERATOR_CHOICES, label=u'Opérateur', initial='or')


class RecipeFilterForm(forms.Form):
    title = forms.CharField(label='Titre', max_length=200, required=False, widget=forms.widgets.HiddenInput)
    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(), label=u"Ingrédients",
                                                 required=False, widget=forms.widgets.MultipleHiddenInput)
    OPERATOR_CHOICES = (
        ('or', u'Ou'),
        ('and', u'Et')
    )
    operator = forms.ChoiceField(choices=OPERATOR_CHOICES, label=u'Opérateur', initial='or',
                                 widget=forms.widgets.HiddenInput)

    ORDER_CHOICES = (
        (1, u'Croissant'),
        (2, u'Décroissant'),
    )
    titleOrder = forms.ChoiceField(choices=ORDER_CHOICES, label=u'Titre', required=False)
    difficultyLevelOrder = forms.ChoiceField(choices=ORDER_CHOICES, label=u"Difficulté de préparation", required=False)
    preparationTimeOrder = forms.ChoiceField(choices=ORDER_CHOICES, label=u'Temps de préparation', required=False)
    noteOrder = forms.ChoiceField(choices=ORDER_CHOICES, label=u'Note Moyenne', required=False)


class RecipeNoteForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('recette', 'note', 'comment')


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('ingredient',)
