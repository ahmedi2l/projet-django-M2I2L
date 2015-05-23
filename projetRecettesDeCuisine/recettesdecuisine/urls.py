from django.conf.urls import patterns, url

from recettesdecuisine import views

from django.contrib.auth import views as aviews

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^ajoutRecettes$', views.ajoutRecette, name='ajoutRecettes'),

                       # url(r'^login/$', views.login, name='login'),
                       # url(r'^auth/$', views.auth_view, name='auth_view'),
                       url(r'^logout/$', views.logout, name='logout'),
                       url(r'^loggedin/$', views.loggedin, name='loggedin'),
                       url(r'^index/$', views.index, name='index'),
                       url(r'^registerUser/$', views.registerUser, name='registerUser'),
                       url(r'^registerUser_success/$', views.registerUser_success, name='registerUser_success'),
                       )
