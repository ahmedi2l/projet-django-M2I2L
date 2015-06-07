from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import RecetteForm

from django.contrib import auth
from recettesdecuisine.forms import RegisterUserForm, RecipeSearchForm, RecipeNoteForm

from recettesdecuisine.models import Recette, Choice
from django.views import generic
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.http import Http404

# Create your views here.

# Generic view pour la liste de toutes les recettes
class RecetteListView(generic.ListView):
    model = Recette

    def get_context_data(self, **kwargs):
        form = RecipeSearchForm()
        context = super(RecetteListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['form'] = form
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
    form = RecipeSearchForm()

    context = {
        'recettesList': recettesList,
        'form': form,
    }
    return render(request, 'recettesdecuisine/index.html', context)


# Affichge détaillé des récettes
def recipeDetail(request, recette_id):
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
            # Remplissage automatique des champs owner et ownerId avant sauvegarde
            form.instance.owner = request.user
            form.instance.ownerId = request.user.id
            form.save()
            return render(request, 'recettesdecuisine/addRecette_success.html', )
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
        'user': request.user,
    }
    return render_to_response('registration/loggedin.html', context)


def logout(request):
    auth.logout(request)
    return render(request, 'registration/loggedout.html',)


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


def recipeSearch(request):
    if request.method == 'GET':
        form = RecipeSearchForm(request.GET)
        if form.is_valid() and request.GET:
            queryTitle = form.cleaned_data['title']
            queryResult = Recette.objects.filter(title__icontains=queryTitle)
            return render(request, "recettesdecuisine/searchResult.html", {
                'form': form,
                'queryResult': queryResult,
                'queryTitle': queryTitle,
            })
    else:
        form = RecipeSearchForm()
    return render(request, "recettesdecuisine/searchResult.html", {'form': form, 'queryResult': "noRequest", })

# Résultat des recherches
def searchResult(request):
    return render(request, "recettesdecuisine/searchResult.html",)

#
class DetailView(generic.DetailView):
    model = Recette
    template_name = 'recettesdecuisine/detail.html'

    def get_context_data(self, **kwargs):
        form = RecipeNoteForm()
        context = super(DetailView, self).get_context_data(**kwargs)
        context['form'] = form
        return context


class ResultsView(generic.DetailView):
    model = Recette
    template_name = 'recettesdecuisine/results.html'

#
def vote(request, recette_id):
    p = get_object_or_404(Recette, pk=recette_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'recettesdecuisine/detail.html', {
            'recette': p,
            'error_message': "Vous avez sélectionner aucune note!",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('recettesdecuisine:results', args=(p.id,)))


def addNote(request) :
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = RecipeNoteForm(request.POST)  # Nous reprenons les données
        if form.is_valid():  # Nous vérifions que les données envoyées sont valides
            # Remplissage automatique des champs owner et ownerId avant sauvegarde
            #form.instance.owner = request.user
            form.save()
            return render(request, 'recettesdecuisine/addNote.html', )
    else:
        form = RecipeNoteForm()

    context = {
        'form': form,
    }
    return render(request, 'recettesdecuisine/addNote.html', context)
