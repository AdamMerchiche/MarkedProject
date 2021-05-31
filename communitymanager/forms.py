from .models import *
from django import forms


# Formulaire permettant la création d'un commentaire.
class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        exclude = ["date_creation","post","auteur"]  # on décidera d'exclure la date de création,
        # ne permettant pas à l'utilisateur d'inscrire un commentaire dans le temps.


# Formulaire permettant la création d'un Post.
class PostForm(forms.ModelForm):
    date_evenement = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M'], required=False)
    commu = forms.CharField(max_length=30, required=True)

    class Meta:
        model = Post
        exclude = ["date_creation", 'communaute', 'auteur']

    # On initialisera notre formulaire dans la vue associée. Néanmoins, on fera attention à deux variables du modèle Post.
    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        evenementiel = cleaned_data['evenementiel']
        date_evenement = cleaned_data["date_evenement"]
        # Les deux variables sont indissociables l'une de l'autre. Sans cocher la case évenement, il sera impossible de mettre une date d'évenement
        # et inversement
        if (evenementiel and date_evenement == None) or (not evenementiel and date_evenement != None):
            self.add_error("date_evenement", "Vous devez inscrire une date d'évenement ou cochez l'option évenement")

        # Verification de l'existence de la communaute
        try:
            c = Communaute.objects.get(name=cleaned_data.get('commu'))
        except Communaute.DoesNotExist:
            raise forms.ValidationError("Cette communaute n'existe pas..")

    def save(self, user):
        nouveau_post = super().save(commit=False)
        nouveau_post.auteur = user
        nouveau_post.communaute = Communaute.objects.get(name=self.cleaned_data.get('commu'))
        nouveau_post.save()
        return nouveau_post

# On a fait le choix ici de créer une formulaire pour la modification du POST. Des alternatives auraient pu être trouvées (en utilisant le même formulaire que pour la création d'un POST)
# Néanmoins, il parait intéressant de créer une formulaire à part, notamment pour exclure certaines variables.

class ModificationPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["auteur", "communaute",
                   "date_creation"]  # On choisit d'exclure logiquement la variable "auteur" et "communaute".
        # En effet, l'utilisateur ne pourra modifier l'auteur d'un POST qu'il a lui même écrit.
        # De la même façon, un POST est partagé sur une communauté précise, et ne doit pas être changé.
        # La date de création apparait ici plutôt
        # comme un choix du designer d'application. On choisira de laisser la date de création
        # puisque par définition nous ne recréons pas le POST.
