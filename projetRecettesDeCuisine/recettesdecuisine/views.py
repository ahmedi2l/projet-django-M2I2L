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

    if request.method == 'POST':
        commentForm = RecetteForm(request.POST, recette_id)
        if commentForm.is_valid():
            c = commentForm.save()
            return HttpResponseRedirect('')
    else:
        commentForm = RecetteForm()

    return render(request, 'recettesdecuisine/recetteDetail.html', {'commentForm': commentForm, 'recette': recette})



    # context = {
    # 'recette': recette,
    #     'commentForm': commentForm,
    # }
    # return render(request, 'recettesdecuisine/recetteDetail.html', context)


# Édition (modification) d'une récette
@login_required()
def editRecipe(request, recipe_id):
    # Vérification si la recette appartient à l'utilisateur
    recette = Recette.objects.get(pk=recipe_id)
    if recette.ownerId != request.user.id:
        return HttpResponseForbidden("Accès interdit")

    editRecipeFormSet = modelformset_factory(Recette, extra=0, can_delete=True, form=RecetteForm, )
    if request.method == 'POST':
        formset = editRecipeFormSet(request.POST, request.FILES, queryset=Recette.objects.filter(pk=recipe_id))
        if formset.is_valid():
            c = formset.save()
            return HttpResponseRedirect('/recettedetail/' + recipe_id)
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


from itertools import chain


def recipeSearch(request):
    if request.method == 'GET':
        form = RecipeSearchForm(request.GET)
        filterform = RecipeFilterForm(request.GET)

        if (form.is_valid() and request.GET):
            searchTitle = form.cleaned_data['title']
            searchIngredients = form.cleaned_data['ingredients']
            searchOperator = form.cleaned_data['operator']

            if searchOperator == "or":
                queryResult = Recette.objects.filter(Q(title__icontains=searchTitle) |
                                                     Q(ingredientsList__in=searchIngredients)).distinct()
            else:
                queryResult = Recette.objects.filter(Q(title__icontains=searchTitle) &
                                                     Q(ingredientsList__in=searchIngredients)).distinct()

            return render(request, "recettesdecuisine/searchResult.html", {
                'form': form,
                'filterform': filterform,
                'queryResult': queryResult,
                'searchTitle': searchTitle,
                'searchIngredients': searchIngredients,
                'searchOperator': searchOperator
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
            searchTitle = filterform.cleaned_data['title']
            searchIngredients = filterform.cleaned_data['ingredients']
            searchOperator = filterform.cleaned_data['operator']

            titleOrder = filterform.cleaned_data['titleOrder']
            difficultyLevelOrder = filterform.cleaned_data['difficultyLevelOrder']
            preparationTimeOrder = filterform.cleaned_data['preparationTimeOrder']

            noteOrder = filterform.cleaned_data['noteOrder']
            seach_title_or_ingredient = Recette.objects.filter(Q(title__icontains=searchTitle) |
                                                               Q(ingredientsList__in=searchIngredients)).distinct()
            seach_title_and_ingredient = Recette.objects.filter(Q(title__icontains=searchTitle) &
                                                                Q(ingredientsList__in=searchIngredients)).distinct()

            if titleOrder == '1':
                orderByTitle = 'title'
                orderByDifficultyLevel = '?'
                orderPreparationTime = '?'
            elif titleOrder == '2':
                orderByTitle = '-title'
                orderByDifficultyLevel = '?'
                orderPreparationTime = '?'

            if difficultyLevelOrder == '1':
                orderByDifficultyLevel = 'difficultyLevel'
                orderByTitle = '?'
                orderPreparationTime = '?'
            elif difficultyLevelOrder == '2':
                orderByDifficultyLevel = '-difficultyLevel'
                orderByTitle = '?'
                orderPreparationTime = '?'

            if preparationTimeOrder == '1':
                orderPreparationTime = 'preparationTime'
                orderByTitle = '?'
                orderByDifficultyLevel = '?'
            elif preparationTimeOrder == '2':
                orderPreparationTime = '-preparationTime'
                orderByTitle = '?'
                orderByDifficultyLevel = '?'

            if searchOperator == "or":
                queryResult = seach_title_or_ingredient.order_by(orderByTitle, orderByDifficultyLevel,
                                                                 orderPreparationTime)
            elif searchOperator == "and":
                queryResult = seach_title_and_ingredient.order_by(orderByTitle, orderByDifficultyLevel,
                                                                  orderPreparationTime)

            return render(request, "recettesdecuisine/searchResult.html", {
                'filterform': filterform,
                'form': form,
                'queryResult': queryResult,
            })
    else:
        filterform = RecipeFilterForm()
        form = RecipeSearchForm()
    return render(request, "recettesdecuisine/searchResult.html",
                  {'filterform': filterform, 'form': form})


# Résultat des recherches
def searchResult(request):
    return render(request, "recettesdecuisine/searchResult.html", )


class EvaluateRecipe(generic.DetailView):
    model = Recette
    template_name = 'recettesdecuisine/evaluateRecipe.html'

    def get_context_data(self, **kwargs):
        form = RecipeNoteForm()
        context = super(EvaluateRecipe, self).get_context_data(**kwargs)
        context['form'] = form
        return context


class EvaluateResults(generic.DetailView):
    model = Recette
    template_name = 'recettesdecuisine/evaluateResults.html'


@login_required()
def vote(request, recette_id):
    p = get_object_or_404(Recette, pk=recette_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'recettesdecuisine/evaluateRecipe.html', {
            'recette': p,
            'error_message': "Vous avez sélectionner aucune note!",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('recettesdecuisine:evaluateResults', args=(p.id,)))


@login_required()
def addNote(request):
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = RecipeNoteForm(request.POST)  # Nous reprenons les données
        if form.is_valid():  # Nous vérifions que les données envoyées sont valides
            # Remplissage automatique des champs owner et ownerId avant sauvegarde
            # form.instance.owner = request.user
            form.save()
            return render(request, 'recettesdecuisine/addNote.html', {'form': form})
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

    return render(request, 'recettesdecuisine/editIngredient.html', {'formset': formset})
