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
        ('simple', 'Simple'),
        ('moyen', 'Moyen'),
        ('difficile', 'Difficile'),
    )
    difficultyLevel = models.CharField("Niveau de difficulté", max_length=30, choices=DIFFICULTY_CHOICES,
                                       default='simple')
    cost = models.DecimalField("Coût (€)", max_digits=5, decimal_places=2, validators=[validators.MinValueValidator(0)])
    # images = FileField(upload_to='images/recettes')
    preparationTime = models.PositiveIntegerField("Temps de préparation (min.)", blank=True, null=True)
    cookTime = models.PositiveIntegerField("Temps de cuisson (min.)", blank=True, null=True)
    restTime = models.PositiveIntegerField("Temps de repos (min.)", blank=True, null=True)
    creationDate = models.DateTimeField("Date de création", auto_now_add=True)
    modificationDate = models.DateTimeField("Date de modification", auto_now=True, default=creationDate)
    ownerId = models.PositiveIntegerField("Id de l'auteur", blank=True)
    owner = models.ForeignKey(User, blank=True, null=True)
    note2 = models.ManyToManyField("Note2", null=True, blank=True, verbose_name=u"Notes2", )


    '''
    ingredientsListe = models.CharField(max_length=200)
    preparationSteps = models.CharField(max_length=200)
    mark = models.CharField(max_length=200)
    comment = models.CharField(max_length=200)
    '''

    def __str__(self):  # __unicode__ on Python 2
        return self.title


class Note(models.Model):
    recette = models.ForeignKey(Recette)
    notes = models.PositiveIntegerField(default=0)

    def __str__(self):  # __unicode__ on Python 2
        return self.notes

class Note2(models.Model):
     class Meta:
         verbose_name="Note2"
         verbose_name_plural="Notes2"
     note2 = models.PositiveIntegerField(u"Note2", blank=True, null=True)
     def __unicode__(self):
         return self.note2






class Commentaire(models.Model):
    recette = models.ForeignKey(Recette)
    commentaires = models.TextField(max_length=200)

    def __str__(self):  # __unicode__ on Python 2
        return self.commentaires