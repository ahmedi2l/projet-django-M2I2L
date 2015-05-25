from django.contrib import admin

from recettesdecuisine.models import Recette

# Register your models here.

class RecetteAdmin(admin.ModelAdmin):
    fields = ('title', 'type', 'difficultyLevel', 'cost', 'preparationTime',
              'cookTime', 'restTime')  # , 'owner')

    # Remplissage automatique du champ owner lors de l'ajout d'une rectte via l'admin
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.ownerId = request.user.id
        obj.save()


admin.site.register(Recette, RecetteAdmin)
