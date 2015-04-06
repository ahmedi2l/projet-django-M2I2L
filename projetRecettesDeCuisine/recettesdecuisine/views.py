from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import RecetteForm

from  django.contrib import auth
from django.core.context_processors import csrf
import sys

# Create your views here.

# @login_required()
def index(request):
    return render(request, 'recettesdecuisine/index.html',)


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
def login(request):
    c={}
    c.update(csrf(request))
    return render_to_response('registration/login.html',c)

def auth_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = auth.authenticate(username=username, password=password)

    context={
        'username':username,
        'password':password,
        'result':user,
    }

    if user is None:
        return render(request,'registration/invalid_login.html',context)

    else:
        return render(request, 'registration/loggedin.html',context)

def loggedin(request):
    return render_to_response('registration/loggedin.html',{'full_name':request.user.username})

def invalid_login(request):
    c={}
    c.update(csrf(request))
    return render_to_response('registration/invalid_login.html', c)

def logout(request):
    return render(request,'registration/logout.html')
