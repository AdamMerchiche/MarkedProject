from .models import*
from django import forms
from django.contrib.auth.models import User


class ConnexionForm(forms.Form):
    username= forms.CharField(label="Nom d'utilisateur")
    password= forms.CharField(label="Mot de passe", widget = forms.PasswordInput)

class Abonnement(forms.Form):
    is_abonne = forms.BooleanField(label = "is_abonne")
    def clean(self):
        cleaned_data = super(Abonnement, self).clean()
        is_abonne = cleaned_data.get("is_abonne")
        return cleaned_data
