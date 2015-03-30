from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from .forms import RecetteForm

# Create your views here.

# @login_required()
def index(request):
    return render(request, 'recettesdecuisine/index.html', locals())


def ajoutRecettes(request):
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        formulaire = RecetteForm(request.POST)  # Nous reprenons les données
        if formulaire.is_valid():  # Nous vérifions que les données envoyées sont valides
            formulaire.save()
    else:
        formulaire = RecetteForm()

    context = {
        'formulaires': formulaire,
    }
    return render(request, 'recettesdecuisine/ajoutRecettes.html', context)

