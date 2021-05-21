from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Communaute(models.Model):
    name = models.CharField(max_length =30)
    abonnes= models.ManyToManyField(User,related_name = "abonnés", blank = True)
    statut = models.BooleanField(default= False)
    def __str__(self):
        return self.name

class Priorite(models.Model):
    labels = models.CharField(max_length =30)
    def __str__(self):
        return self.labels

class Post(models.Model):
    description = models.CharField(max_length = 250)
    title = models.CharField(max_length = 250, blank = True)
    date_creation = models.DateTimeField(default=timezone.now,
                                verbose_name="Date du commentaire")
    evenementiel = models.BooleanField(default= False)
    date_evenement = models.DateTimeField(default=timezone.now,
                                         verbose_name="Date de l'évenement")
    communaute = models.ForeignKey(Communaute, on_delete="models.CASCADE")
    priorite = models.ForeignKey(Priorite, on_delete="models.CASCADE")
    auteur = models.ForeignKey(User, on_delete= "models.CASCADE")
