from .models import*
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone


class ConnexionForm(forms.Form):
    username= forms.CharField(label="Nom d'utilisateur")
    password= forms.CharField(label="Mot de passe", widget = forms.PasswordInput)

class Abonnement(forms.Form):
    is_abonne = forms.BooleanField(label = "is_abonne")
    def clean(self):
        cleaned_data = super(Abonnement, self).clean()
        is_abonne = cleaned_data.get("is_abonne")
        return cleaned_data

class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = "__all__"


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"

    def clean(self):
        """
        Validates a new album only if it's not a duplicate
        """
        cleaned_data = super(PostForm, self).clean()
        evenementiel = cleaned_data['evenementiel']
        date_evenement= cleaned_data["date_evenement"]

        if evenementiel and date_evenement==None :
            raise forms.ValidationError("Vous devez inscrire une date d'évenement")
        return cleaned_data

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["auteur", "communaute", "date_creation"]

