from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import RecetteForm

from django.contrib import auth
from django.core.context_processors import csrf
from recettesdecuisine.forms import RegisterUserForm

# Create your views here.

def index(request):
    return render(request, 'recettesdecuisine/index.html', )

# Ajout d'une recette
def ajoutRecette(request):
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

@login_required()
def loggedin(request):
    context = {
        'username': request.user.username
    }
    return render_to_response('registration/loggedin.html', context)

def logout(request):
    return render(request, 'registration/logged_out.html')


# Création d'un compte utilisateur
def registerUser(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/registerUser_success")
    else:
        form = RegisterUserForm()
    return render(request, "registration/registerUser.html", {
        'form': form,
    })


def registerUser_success(request):
    return render(request, 'registration/registerUser_success.html', )


'''
#Ancienne méthonde de création d'un utilisateur
def registerUser(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                return render(request, 'registration/registerUser_success.html', {'username': username, 'message': u"Le compte a été crée"})
            except :
                return render(request, 'registration/registerUser_success.html', {'username': username, 'message': u"Le compte n'a pas pu être créé"})
    else:
        form = RegisterUserForm()

    context = {
        'form': form,
    }
    return render(request, 'registration/registerUser.html', context)
'''