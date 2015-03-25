from django.conf.urls import patterns, url

from recettesdecuisine import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^ajoutRecettes$', views.ajoutRecettes, name='ajoutRecettes'),
)
