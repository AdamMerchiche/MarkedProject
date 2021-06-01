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
    date_evenement = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S'], required=False)
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
            self.add_error("commu", "Cette communaute n'existe pas..")

        return super().clean()



    def save(self, user):
        nouveau_post = super().save(commit=False)
        nouveau_post.auteur = user
        nouveau_post.communaute = Communaute.objects.get(name=self.cleaned_data.get('commu'))
        nouveau_post.save()
        return nouveau_post

    def modifPost(self, id):
        cleaned_data = self.clean()
        modif_post = Post.objects.filter(id=id)
        modif_post.update(title=cleaned_data.get('title'),
                                priorite=cleaned_data.get('priorite'),
                                evenementiel=cleaned_data.get('evenementiel'),
                                date_evenement=cleaned_data.get('date_evenement'),
                                communaute=Communaute.objects.filter(name=cleaned_data.get('commu'))[0],
                                description=cleaned_data.get('description'),)
        return modif_post[0]


