from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .forms import RecetteForm, IngredientForm

from django.contrib import auth
from recettesdecuisine.forms import RegisterUserForm, RecipeSearchForm, RecipeFilterForm, RecipeNoteForm

from recettesdecuisine.models import Recette, Choice, Ingredient
from django.views import generic
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.db.models import Q


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

# Édition (modification) d'une récette
@login_required()
def editRecipe(request, recipe_id):

    # Vérification si la recette appartient à l'utilisateur
    recette = Recette.objects.get(pk=recipe_id)
    if recette.ownerId != request.user.id :
        return HttpResponseForbidden("Accès interdit")

    editRecipeFormSet = modelformset_factory(Recette, extra=0, can_delete=True, form=RecetteForm,)
    if request.method == 'POST':
        formset = editRecipeFormSet(request.POST, request.FILES, queryset=Recette.objects.filter(pk=recipe_id))
        if formset.is_valid():
            c = formset.save()
            return HttpResponseRedirect('/recettedetail/'+recipe_id)
    else:
        formset = editRecipeFormSet(queryset=Recette.objects.filter(pk=recipe_id))

    return render(request, 'recettesdecuisine/editRecipe.html', {'formset': formset, 'recipe_id': recipe_id})


# Ajout d'une recette
@login_required()
def addRecette(request):
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = RecetteForm(request.POST, request.FILES)  # Nous reprenons les données
        if form.is_valid():  # Nous vérifions que les données envoyées sont valides
            # Remplissage automatique des champs owner et ownerId avant sauvegarde
            form.instance.owner = request.user
            form.instance.ownerId = request.user.id
            form.save()
            return render(request, 'recettesdecuisine/addRecette_success.html', )
    else:
        form = RecetteForm()
        addIngredientForm = IngredientForm(request.POST)

    context = {
        'form': form,
    }
    return render(request, 'recettesdecuisine/addRecette.html', context)


@login_required()
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
    return render(request, 'registration/loggedout.html', )


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
        filterform = RecipeFilterForm(request.GET)

        if (form.is_valid() and request.GET):
            searchTitle = form.cleaned_data['title']
            searchIngredients = form.cleaned_data['ingredients']

            queryResult = Recette.objects.filter(Q(title__icontains=searchTitle) | Q(ingredientsList__in=searchIngredients))
            return render(request, "recettesdecuisine/searchResult.html", {
                'form': form,
                'filterform': filterform,
                'queryResult': queryResult,
                'searchTitle': searchTitle,
            })
    else:
        form = RecipeSearchForm()
    return render(request, "recettesdecuisine/searchResult.html",
                  {'form': form, 'filterform': filterform, 'queryResult': "noRequest", })


def recipeSearchFilter(request):
    if request.method == 'GET':
        filterform = RecipeFilterForm(request.GET)
        form = RecipeSearchForm(request.GET)

        if (filterform.is_valid() and request.GET):
            filterTitle = filterform.cleaned_data['title']
            filterIngredients = filterform.cleaned_data['ingredients']
            filterByDifficultyLevel = filterform.cleaned_data['difficultyLevel']
            filterByTitleOrder = filterform.cleaned_data['titleOrder']
            filterByNote = filterform.cleaned_data['note']
            filterByPreparationTime = filterform.cleaned_data['preparationTime']

            if filterByTitleOrder != '1':
                queryResult = Recette.objects.filter(Q(title__icontains=filterTitle) | Q(ingredientsList__in=filterIngredients)).order_by('-title')
            elif filterByPreparationTime != '1':
                queryResult = Recette.objects.filter(Q(title__icontains=filterTitle) | Q(ingredientsList__in=filterIngredients)).order_by('-preparationTime')
            elif filterByNote != '1':
                queryResult = Recette.objects.filter(Q(title__icontains=filterTitle) | Q(ingredientsList__in=filterIngredients)).order_by('-note')
            else:
                queryResult = Recette.objects.filter(Q(title__icontains=filterTitle) | Q(ingredientsList__in=filterIngredients))

            return render(request, "recettesdecuisine/searchResult.html", {
                'filterform': filterform,
                'form': form,
                'queryResult': queryResult,
            })
    else:
        filterform = RecipeFilterForm()
        form = RecipeSearchForm()
    return render(request, "recettesdecuisine/searchResult.html",
                  {'filterform': filterform, 'form': form, 'queryResult': "noRequest"})


# Résultat des recherches
def searchResult(request):
    return render(request, "recettesdecuisine/searchResult.html", )


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


@login_required()
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


@login_required()
def addNote(request):
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = RecipeNoteForm(request.POST)  # Nous reprenons les données
        if form.is_valid():  # Nous vérifions que les données envoyées sont valides
            # Remplissage automatique des champs owner et ownerId avant sauvegarde
            # form.instance.owner = request.user
            form.save()
            return render(request, 'recettesdecuisine/addNote.html', )
    else:
        form = RecipeNoteForm()

    context = {
        'form': form,
    }
    return render(request, 'recettesdecuisine/addNote.html', context)


@login_required()
def addIngredient(request):
    if request.method == 'POST':
        addIngredientForm = IngredientForm(request.POST)
        if addIngredientForm.is_valid():
            c = addIngredientForm.clean()
            c = addIngredientForm.save()

            return HttpResponseRedirect('/addRecette')
    else:
        addIngredientForm = IngredientForm()

    return render(request, 'recettesdecuisine/addIngredient.html', {'addIngredientForm': addIngredientForm, })

def editIngredient(request):

    ingregientFormSet = modelformset_factory(Ingredient, extra=0, can_delete=True, form=IngredientForm)

    if request.method == 'POST':
        formset = ingregientFormSet(request.POST, request.FILES)
        if formset.is_valid():
            c = formset.save()
            return HttpResponseRedirect('/addRecette')
    else:
        formset = ingregientFormSet()

    return render(request,'recettesdecuisine/editIngredient.html', {'formset': formset})


