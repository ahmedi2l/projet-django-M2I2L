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

                       url(r'^recetteList$', views.RecetteListView.as_view(), name='recetteList'),
                       url(r'^recettedetail/(?P<recette_id>\d+)/$', views.recipeDetail, name='recipeDetail'),

                       url(r'^recipeSearch/$', views.recipeSearch, name='recipeSearch'),
                       url(r'^searchResult/$', views.searchResult, name='searchResult'),

                       # ex: /5/
                       url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
                       # ex: /5/results/
                       url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
                       # ex: /5/vote/
                       url(r'^(?P<recette_id>\d+)/vote/$', views.vote, name='vote'),

                       url(r'^addNote/$', views.addNote, name='addNote'),

                       )
