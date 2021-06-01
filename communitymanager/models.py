from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone, dateformat


# Modèle définissant la Communauté. On la caractérise par ses abonnés, et son nom.
class Communaute(models.Model):
    name = models.CharField(max_length=30)
    abonnes = models.ManyToManyField(User, related_name="abonnements", blank=True)
    def __str__(self):
        return self.name


# Modèle caractérisant la priorité des POSTs. On essaiera, dans un deuxième temps, d'associer la priorité à une couleur.
class Priorite(models.Model):
    labels = models.CharField(max_length=30)

    def __str__(self):
        return self.labels


# Modèle du POST, renseignant l'ensemble des variables demandées.
class Post(models.Model):
    description = models.TextField()  # On préfèrera un TextField afin de ne pas limiter le POST
    title = models.CharField(max_length=250, blank=False)
    date_creation = models.DateTimeField(default=timezone.now,
                                         verbose_name="Date du post")
    evenementiel = models.BooleanField(default=False,
                                       blank=True)  # Les deux variables sont ici non requises pour un POST.
    date_evenement = models.DateTimeField(verbose_name="Date de l'évenement", blank=True, null=True)

    communaute = models.ForeignKey(Communaute, on_delete="models.CASCADE")
    priorite = models.ForeignKey(Priorite, on_delete="models.CASCADE")
    auteur = models.ForeignKey(User, on_delete="models.CASCADE", related_name="posts")

    # On choisira d'ordonner l'ensemble des POSTs en fonction de leur date de publication.
    # Plus un POST est ancien, plus il faudra descendre sur la page pour le voir.
    class Meta:
        ordering = ['-date_creation']


# Modèle du Commentaire, renseignant l'ensemble des variables demandées.
class Commentaire(models.Model):
    date_creation = models.DateTimeField(default=timezone.now,
                                         verbose_name="Date du commentaire")
    contenu = models.TextField()
    auteur = models.ForeignKey(User, on_delete="models.CASCADE")
    post = models.ForeignKey(Post, on_delete="models.CASCADE")

    # A l'image d'un Forum, on choisira plutôt d'ordonner les commentaires de façon différente. Les commentaires les plus anciens apparaisseront en haut de page.
    class Meta:
        ordering = ['date_creation']
