from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Modèle définissant la Communauté. On la caractérise par ses abonnés, et son nom.
class Communaute(models.Model):
    name = models.CharField(max_length=30)
    abonnes = models.ManyToManyField(User, related_name="abonnements", blank=True)
    list_bannis = models.ManyToManyField(User, related_name="bannis", blank=True)
    list_CMs = models.ManyToManyField(User, related_name="CMs", blank=True)
    createur = models.ForeignKey(User, on_delete="models.DO_NOTHING")
    description = models.CharField(max_length=2500, blank=False)
    ferme= models.BooleanField(default=False)
    ferme_invisible = models.BooleanField(default=False)
    def __str__(self):
        return self.name


# Modèle caractérisant la priorité des POSTs. On essaiera, dans un deuxième temps, d'associer la priorité à une couleur.
class Priorite(models.Model):
    labels = models.CharField(max_length=30)
    rang = models.IntegerField() # la priorite la plus haute a pour rang 1

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

    communaute = models.ForeignKey(Communaute, on_delete=models.CASCADE)
    priorite = models.ForeignKey(Priorite, on_delete=models.DO_NOTHING)
    auteur = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    collant = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
    avertissement = models.BooleanField(default=False)
    lecteurs = models.ManyToManyField(User, related_name="lecteurs", blank=True)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)

    # On choisira d'ordonner l'ensemble des POSTs en fonction de leur date de publication.
    # Plus un POST est ancien, plus il faudra descendre sur la page pour le voir.
    class Meta:
        ordering = ['-avertissement','-collant', '-date_creation']


# Modèle du Commentaire, renseignant l'ensemble des variables demandées.
class Commentaire(models.Model):
    date_creation = models.DateTimeField(default=timezone.now,
                                         verbose_name="Date du commentaire")
    contenu = models.TextField()
    auteur = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    invisible = models.BooleanField(default=False)

    # A l'image d'un Forum, on choisira plutôt d'ordonner les commentaires de façon différente. Les commentaires les plus anciens apparaisseront en haut de page.
    class Meta:
        ordering = ['date_creation']
