# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from recettesdecuisine.models import Recette

class RecetteAdmin(admin.ModelAdmin):
    fields = []

admin.site.register(Recette, RecetteAdmin)

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'', include('recettesdecuisine.urls', namespace="recettesdecuisine")),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
)
