from django.db import models
from django.core import validators


# Create your models here.



class Recette(models.Model):
    title = models.CharField(max_length=200, unique=True)
    TYPE_CHOICES=(
        ('entre','Entrée'),
        ('platPrincipal','Plat principal'),
        ('dessert','Dessert'),
    )
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='platPrincipal')
    DIFFICULTY_CHOICES=(
        ('simple','Simple'),
        ('moyen','Moyen'),
        ('difficile','Difficile'),
    )
    difficulty = models.CharField(max_length=30, choices=DIFFICULTY_CHOICES, default='simple')
    cost = models.DecimalField(max_digits=5, decimal_places=2, validators=[validators.MinValueValidator(0)])
    #images = FileField(upload_to='images/recettes')
    preparationTime = models.PositiveIntegerField(blank=True, null=True)
    cookTime = models.PositiveIntegerField(blank=True, null=True)
    restTime = models.PositiveIntegerField(blank=True, null=True)

    '''
    ingredientsListe = models.CharField(max_length=200)
    preparationSteps = models.CharField(max_length=200)
    mark = models.CharField(max_length=200)
    comment = models.CharField(max_length=200)
    '''

    def __str__(self):              # __unicode__ on Python 2
        return self.title