from .models import *
from django import forms


# Formulaire permettant la création d'un commentaire.
class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        exclude = ["date_creation", "post", "auteur"]  # on décidera d'exclure la date de création,
        # ne permettant pas à l'utilisateur d'inscrire un commentaire dans le temps.


# Formulaire permettant la création d'un Post.
class PostForm(forms.ModelForm):
    date_evenement = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S'], required=False)
    commu = forms.CharField(max_length=30, required=True)

    class Meta:
        model = Post
        exclude = ["date_creation", 'communaute', 'auteur', 'visible', "lecteurs", "likes"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PostForm, self).__init__(*args, **kwargs)

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
            communaute = Communaute.objects.get(name=self.cleaned_data.get('commu'))
        except Communaute.DoesNotExist:
            self.add_error("commu", "Cette communaute n'existe pas!")
            communaute = None
        except:
            communaute = Communaute.objects.filter(name=self.cleaned_data.get('commu'))[0]
        # Verification que l'utilisateur soit abonne pour poster dans une communaute s'il force l'acces
        else:
            if communaute not in self.user.abonnements.all():
                self.add_error("commu",
                               "Vous ne pouvez pas poster dans cette communaute car vous n'etes pas abonne!")
            collant = cleaned_data["collant"]
            avertissement = cleaned_data["avertissement"]
            duplicat = Post.objects.filter(communaute_id=communaute.id).filter(collant=True)


            if collant and duplicat.exists():
                self.add_error("collant", "Un post de la communauté est déjà collé! Veuillez réctifier la situation. ")

            if collant and not self.user in communaute.list_CMs.all():
                self.add_error("collant", "Vous ne pouvez pas coller votre POST car vous n'êtes pas un CM. ")


        return super().clean()

    def save(self, user):
        nouveau_post = super().save(commit=False)
        nouveau_post.auteur = user
        nouveau_post.communaute = Communaute.objects.filter(name=self.cleaned_data.get('commu'))[0]
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
                          description=cleaned_data.get('description'),
                          collant=cleaned_data.get('collant'),
                          avertissement=cleaned_data.get('avertissement'),)
        return modif_post[0]


class CommunauteForm(forms.ModelForm):
    class Meta:
        model = Communaute
        exclude = ["list_bannis", "abonnes", "ferme_invisible", 'createur']

    def save(self, user):
        nouvelle_communaute = super().save(commit=False)
        nouvelle_communaute.createur = user
        nouvelle_communaute.save()
        return nouvelle_communaute



class ModificationCommunauteForm(forms.ModelForm):
    class Meta:
        model = Communaute
        exclude = ["createur", "abonnes",
                   "ferme_invisible", "list_CMs"]  # Possible de modifier la description, le titre, et de bannir des abonnés de la commu


class FiltragePostCommunauteForm(forms.Form):
    type_filtrage = forms.ChoiceField(choices=[('OU', 'ou'), ('ET', 'et')])
    min_priorite = forms.ModelChoiceField(queryset=Priorite.objects.all(), empty_label="(Vide)", required=False)
    que_evt = forms.BooleanField(required=False)

class SimpleSearchForm(forms.Form):
    simple_query = forms.CharField(max_length=50, label='Rechercher')

class SearchForm(forms.Form):
    query = forms.CharField(max_length=50, required=False, label='Rechercher')
    is_global = forms.BooleanField(required=False)
    is_post = forms.BooleanField(required=False)
    is_commu = forms.BooleanField(required=False)
    date_evnt = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S'], required=False)
    date_post = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S'], required=False)

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()


