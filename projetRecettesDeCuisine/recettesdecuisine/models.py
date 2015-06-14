from django.db import models
from django.core import validators

from django.contrib.auth.models import User


# Create your models here.

class Recette(models.Model):
    title = models.CharField("Titre", max_length=200, unique=True)
    TYPE_CHOICES = (
        ('entre', 'Entrée'),
        ('platPrincipal', 'Plat principal'),
        ('dessert', 'Dessert'),
    )
    type = models.CharField("Type", max_length=30, choices=TYPE_CHOICES, default='platPrincipal', editable=True)
    DIFFICULTY_CHOICES = (
        (1, u'Simple'),
        (2, u'Moyen'),
        (3, u'Difficile'),
    )
    difficultyLevel = models.IntegerField("Niveau de difficulté", max_length=30, choices=DIFFICULTY_CHOICES,
                                       default='Simple')
    cost = models.DecimalField("Coût (€)", max_digits=5, decimal_places=2,
                               validators=[validators.MinValueValidator(0)], blank=True, null=True)
    images = models.ImageField(upload_to="images", default='images/image_non_disponible.png')
    preparationTime = models.PositiveIntegerField("Temps de préparation (min.)", blank=True, null=True)
    cookTime = models.PositiveIntegerField("Temps de cuisson (min.)", blank=True, null=True)
    restTime = models.PositiveIntegerField("Temps de repos (min.)", blank=True, null=True)
    creationDate = models.DateTimeField("Date de création", auto_now_add=True)
    modificationDate = models.DateTimeField("Date de modification", auto_now=True, default=creationDate)
    ownerId = models.PositiveIntegerField("Id de l'auteur", blank=True)
    owner = models.ForeignKey(User, blank=True, null=True)
    ingredientsList = models.ManyToManyField("Ingredient", null=True, blank=True, verbose_name=u"Ingrédients")
    '''
    preparationSteps = models.CharField(max_length=200)
    mark = models.CharField(max_length=200)
    comment = models.CharField(max_length=200)
    '''

    def __str__(self):  # __unicode__ on Python 2
        return self.title


class Choice(models.Model):
    recette = models.ForeignKey(Recette)
    # comment = models.TextField("Commentaire", max_length=200, blank=True, null=True)
    NOTES_CHOICES = [(i, i) for i in range(11)]
    note = models.PositiveIntegerField("Note", choices=NOTES_CHOICES)
    votes = models.IntegerField(default=0)

    def __int__(self):  # __unicode__ on Python 2
        return self.note


class Ingredient(models.Model):
    class Meta:
        verbose_name = "Ingrédient"
        verbose_name_plural = "Ingrédients"

    ingredient = models.CharField(u"Ingrédient", max_length=30, unique=True)

    def __str__(self):
        return self.ingredient
