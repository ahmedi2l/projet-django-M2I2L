# -*- coding:utf-8 -*-
from django.contrib import admin

from recettesdecuisine.models import Recette, Choice

# Register your models here.

class NoteInline(admin.TabularInline):
    model = Choice
    extra = 1


class RecetteAdmin(admin.ModelAdmin):
    fieldsets = [
        ('La recette', {'fields': ['title', 'type', 'difficultyLevel', 'cost']}),
        ('Informations sur les temps ', {'fields': ['preparationTime', 'cookTime', 'restTime'],
                                         'classes': ['collapse']}),
        # fields = ('title', 'type', 'difficultyLevel', 'cost', 'preparationTime',
        #              'cookTime', 'restTime')  # , 'owner', 'ownerId')
    ]
    inlines = [NoteInline]

    # Champs à afficher
    list_display = ('title', 'type', 'difficultyLevel', 'cost', 'preparationTime',
                    'cookTime', 'restTime')  # , 'owner', 'ownerId')
    # Filtre de tri
    list_filter = ['type', 'difficultyLevel', 'cost', 'preparationTime', 'cookTime', 'restTime']

    # Champs de recherche
    search_fields = ['title', ]

    # Remplissage automatique du champ owner lors de l'ajout d'une rectte via l'admin
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.ownerId = request.user.id
        obj.save()


admin.site.register(Recette, RecetteAdmin)

