from django.conf.urls import patterns, url

from recettesdecuisine import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
                       # url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
                       url(r'^logout/$', views.logout, name='logout'),
                       url(r'^loggedin/$', views.loggedin, name='loggedin'),
                       url(r'^index/$', views.index, name='index'),
                       url(r'^registerUser/$', views.registerUser, name='registerUser'),
                       url(r'^registerUser_success/$', views.registerUser_success, name='registerUser_success'),
                       url(r'^addRecette$', views.addRecette, name='addRecette'),
                       url(r'^addRecette_success/$', views.addRecette_success, name='addRecette_success'),
                       url(r'^addIngredient/$', views.addIngredient, name='addIngredient'),
                       url(r'^editIngredient/$', views.editIngredient, name='editIngredient'),
                       url(r'^editRecipe/(?P<recipe_id>\d+)/$', views.editRecipe, name='editRecipe'),
                       url(r'^recetteList$', views.RecetteListView.as_view(), name='recetteList'),
                       url(r'^recettedetail/(?P<recette_id>\d+)/$', views.recipeDetail, name='recipeDetail'),

                       url(r'^recipeSearch/$', views.recipeSearch, name='recipeSearch'),
                       url(r'^recipeSearchFilter/$', views.recipeSearchFilter, name='recipeSearchFilter'),
                       url(r'^searchResult/$', views.searchResult, name='searchResult'),

                       # ex: evaluateRecipe/5/
                       url(r'^evaluateRecipe/(?P<pk>\d+)/$', views.EvaluateRecipe.as_view(), name='evaluateRecipe'),
                       # ex: evaluateResults/5/results/
                       url(r'^evaluateResults/(?P<pk>\d+)/results/$', views.EvaluateResults.as_view(), name='evaluateResults'),
                       # ex: /5/vote/
                       url(r'^(?P<recette_id>\d+)/vote/$', views.vote, name='vote'),

                       url(r'^addNote/$', views.addNote, name='addNote'),
                       #url(r'^addComment/(?P<recipe_id>\d+)/$', views.addComment, name='addComment'),

                       )
