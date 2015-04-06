from django.conf.urls import patterns, url

from recettesdecuisine import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^ajoutRecettes$', views.ajoutRecettes, name='ajoutRecettes'),

    url(r'^login/$', views.login, name='login'),
    url(r'^auth/$', views.auth_view, name='auth_view'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^loggedin/$', views.loggedin, name='loggedin'),
    url(r'^invalid_login/$', views.invalid_login, name='invalid_login'),

)
