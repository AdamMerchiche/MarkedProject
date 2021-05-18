from .models import*
from django import forms


class ConnexionForm(forms.Form):
    username= forms.CharField(label="Nom d'utilisateur")
    password= forms.CharField(label="Mot de passe", widget = forms.PasswordInput)

