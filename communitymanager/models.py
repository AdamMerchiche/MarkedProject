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
    description = models.TextField()
    title = models.CharField(max_length = 250, blank = False)
    date_creation = models.DateTimeField(default=timezone.now,
                                verbose_name="Date du post", blank=True)
    evenementiel = models.BooleanField(default= False, blank=True)
    date_evenement = models.DateTimeField(verbose_name="Date de l'évenement", blank=True, null=True)

    communaute = models.ForeignKey(Communaute, on_delete="models.CASCADE")
    priorite = models.ForeignKey(Priorite, on_delete="models.CASCADE")
    auteur = models.ForeignKey(User, on_delete= "models.CASCADE")
    class Meta:
        """Classe qui caractérise le comportement des modèles : verbose =
        ce que représente le modèle ; ordering = ordre par défaut de la sélection. """
        ordering = ['date_creation']


class Commentaire(models.Model):
    date_creation = models.DateTimeField(default=timezone.now,
                                         verbose_name="Date du commentaire")
    contenu = models.TextField()
    auteur = models.ForeignKey(User, on_delete= "models.CASCADE")
    post = models.ForeignKey(Post, on_delete= "models.CASCADE")


