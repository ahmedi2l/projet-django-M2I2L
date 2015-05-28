from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import RecetteForm

from django.contrib import auth
from django.core.context_processors import csrf
from recettesdecuisine.forms import RegisterUserForm, RecetteSearchForm

from recettesdecuisine.models import Recette
from django.views.generic.list import ListView
from django.utils import timezone
from django.views.generic.detail import DetailView

from django.contrib.auth.models import User

# Create your views here.

# Generic view pour la liste de toutes les recettes
class RecetteListView(ListView):
    model = Recette

    def get_context_data(self, **kwargs):
        context = super(RecetteListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


def loggedUserMessage(request):
    username = request.user.username
    if username == "":
        return None
    else:
        return "Bonjour " + username


# Page d'accueil
def index(request):
    # Affichage des 5 dernières recettes en page d'accueil
    recettesList = Recette.objects.all().order_by('-id')[:5]

    context = {
        'recettesList': recettesList,
        'loggedUserMessage': loggedUserMessage(request)
    }
    return render(request, 'recettesdecuisine/index.html', context)


# Affichge détaillé des récettes
def recetteDetail(request, recette_id):
    recette = Recette.objects.get(pk=recette_id)

    context = {
        'recette': recette,
    }
    return render(request, 'recettesdecuisine/recetteDetail.html', context)


# Ajout d'une recette
@login_required()
def addRecette(request):
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = RecetteForm(request.POST)  # Nous reprenons les données
        if form.is_valid():  # Nous vérifions que les données envoyées sont valides
            try:
                # Remplissage automatique des champs owner et ownerId avant sauvegarde
                form.instance.owner = request.user
                form.instance.ownerId = request.user.id
                form.save()
                return render(request, 'recettesdecuisine/addRecette_success.html', )
            except:
                pass
    else:
        form = RecetteForm()

    context = {
        'form': form,
    }
    return render(request, 'recettesdecuisine/addRecette.html', context)


def addRecette_success(request):
    return render(request, 'recettesdecuisine/addRecette_success.html', )


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


def recetteSearch(request):
    if request.method == 'GET':
        form = RecetteSearchForm(request.GET)
        if form.is_valid() and request.GET:
            queryResult = Recette.objects.filter(title__icontains=form.cleaned_data['title'])
            return render(request, "recettesdecuisine/recetteSearch.html", {
                'form': form,
                'queryResult': queryResult,
            })
    else:
        form = RecetteSearchForm()
    return render(request, "recettesdecuisine/recetteSearch.html", {'form': form, 'queryResult': "noRequest", })


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

