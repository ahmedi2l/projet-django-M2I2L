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
    type = models.CharField("Type", max_length=30, choices=TYPE_CHOICES, default='platPrincipal')
    DIFFICULTY_CHOICES = (
        ('simple', 'Simple'),
        ('moyen', 'Moyen'),
        ('difficile', 'Difficile'),
    )
    difficultyLevel = models.CharField("Niveau de difficulté", max_length=30, choices=DIFFICULTY_CHOICES, default='simple')
    cost = models.DecimalField("Coût (€)", max_digits=5, decimal_places=2, validators=[validators.MinValueValidator(0)])
    # images = FileField(upload_to='images/recettes')
    preparationTime = models.PositiveIntegerField("Temps de préparation (min.)", blank=True, null=True)
    cookTime = models.PositiveIntegerField("Temps de cuisson (min.)", blank=True, null=True)
    restTime = models.PositiveIntegerField("Temps de repos (min.)", blank=True, null=True)
    creationDate = models.DateTimeField("Date de création", auto_now_add=True)
    modificationDate = models.DateTimeField("Date de modification", auto_now=True, default=creationDate)
    ownerId = models.PositiveIntegerField("Id de l'auteur", blank=True)
    owner = models.ForeignKey(User, blank=True,null=True)

    '''
    ingredientsListe = models.CharField(max_length=200)
    preparationSteps = models.CharField(max_length=200)
    mark = models.CharField(max_length=200)
    comment = models.CharField(max_length=200)
    '''

    def __str__(self):  # __unicode__ on Python 2
        return self.title
