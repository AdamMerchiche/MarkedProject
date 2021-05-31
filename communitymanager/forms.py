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
    class Meta:
        model = Post
        exclude = ["date_creation"]


    # On initialisera notre formulaire dans la vue associée. Néanmoins, on fera attention à deux variables du modèle Post.
    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        evenementiel = cleaned_data['evenementiel']
        date_evenement = cleaned_data["date_evenement"]
        collant = cleaned_data["collant"]
        communaute =cleaned_data["communaute"]
        duplicat = Post.objects.filter(communaute_id=communaute.id).filter(collant=True)
        if duplicat.exists():
            raise forms.ValidationError("Un post de la communauté est déjà collé! Veuillez réctifier la situation. ")
        # Les deux variables sont indissociables l'une de l'autre. Sans cocher la case évenement, il sera impossible de mettre une date d'évenement
        # et inversement
        if (evenementiel and date_evenement == None) or (not evenementiel and date_evenement != None):
            raise forms.ValidationError("Vous devez inscrire une date d'évenement ou cochez l'option évenement")
        return cleaned_data


# On a fait le choix ici de créer une formulaire pour la modification du POST. Des alternatives auraient pu être trouvées (en utilisant le même formulaire que pour la création d'un POST)
# Néanmoins, il parait intéressant de créer une formulaire à part, notamment pour exclure certaines variables.

class ModificationPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["auteur","date_creation"]  # On choisit d'exclure logiquement la variable "auteur".
        # En effet, l'utilisateur ne pourra modifier l'auteur d'un POST qu'il a lui même écrit.
        # La date de création apparait ici plutôt
        # comme un choix du designer d'application. On choisira de laisser la date de création
        # puisque par définition nous ne recréons pas le POST.
    def clean(self):
        cleaned_data = super(ModificationPostForm, self).clean()
        collant = cleaned_data["collant"]
        communaute = cleaned_data["communaute"]
        duplicat = Post.objects.filter(communaute_id=communaute.id).filter(collant=True)
        if duplicat.exists():
            raise forms.ValidationError("Un post de la communauté est déjà collé! Veuillez réctifier la situation. ")
        if (evenementiel and date_evenement == None) or (not evenementiel and date_evenement != None):
            raise forms.ValidationError("Vous devez inscrire une date d'évenement ou cochez l'option évenement")
        return cleaned_data

class CommunauteForm(forms.ModelForm):
    class Meta:
        model = Communaute
        fields = "__all__"

class ModificationCommunauteForm(forms.ModelForm):
    class Meta:
        model = Communaute
        exclude = ["createur"] #Possible de modifier la description, le titre, et de bannir des abonnés de la commu
