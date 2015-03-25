from django.db import models
from django.forms import ModelForm
from .models import Recette

class RecetteForm(ModelForm):
    class Meta:
        model = Recette
        fields = ['title', 'type']