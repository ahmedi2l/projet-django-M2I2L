from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import RecetteForm

from  django.contrib import auth
from django.core.context_processors import csrf
from recettesdecuisine.forms import LoginForm

# Create your views here.

# @login_required()
def index(request):
    return render(request, 'recettesdecuisine/index.html', )


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


###
"""
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = auth.authenticate(username=username, password=password)

            context = {
                'username': username,
                'password': password,
                'result': user,
            }

            if user is None:
                return render(request, 'registration/login_ok.html', context)
            else:
                return render(request, 'registration/loggedin.html', context)

    else:
        form = LoginForm()

    context = {
        'form': form,
    }
    return render(request, 'registration/login_ok.html', context)
"""

###
@login_required()
def loggedin(request):
    context = {
        'username': request.user.username
    }
    return render_to_response('registration/loggedin.html', context)


def logout(request):
    return render(request, 'registration/logged_out.html')
