from django.db import models

# Create your models here.

class Recette(models.Model):
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

    def __str__(self):              # __unicode__ on Python 2
        return self.title