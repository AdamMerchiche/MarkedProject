from .models import*
from django import forms


class ConnexionForm(forms.Form):
    username= forms.CharField(label="Nom d'utilisateur")
    password= forms.CharField(label="Mot de passe", widget = forms.PasswordInput)

class Abonnement(forms.Form):
    statut = forms.BooleanField(label = "Abonné")
    def clean(self):
        cleaned_data = super(Abonnement, self).clean()
        statut = cleaned_data.get("statut")
        return cleaned_data
