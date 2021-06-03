from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import Http404


# Renvoie le feed d'un utilisateur, avec tous les posts des communautés auxquelles il est abonné
@login_required(login_url='/accounts/login/')
def accueil(request):
    date_now = timezone.now()

    communautes = Communaute.objects.filter(abonnes=request.user)
    posts = Post.objects.filter(communaute__abonnes=request.user)
    return render(request, 'communitymanager/feed_abonnements.html', locals())


# Renvoie la liste de toutes les communautés
@login_required(login_url='/accounts/login/')
def liste_communautes(request):
    date_now = timezone.now()
    communautes = Communaute.objects.all()
    communautes = [(commu, Post.objects.filter(communaute=commu).exclude(lecteurs__username=request.user.username).count()) for commu in communautes]
    return render(request, 'communitymanager/list_communautes.html', {'communautes': communautes})


# Permet à l'utilisateur de s'abonner ou se désabonner d'une communauté
@login_required(login_url='/accounts/login/')
def abonner(request, communaute_id):
    date_now = timezone.now()

    communaute = Communaute.objects.get(id=communaute_id)
    if request.user in communaute.abonnes.all():
        communaute.abonnes.remove(request.user)
    else:
        if not request.user in communaute.list_bannis.all():
            communaute.abonnes.add(request.user)
    return redirect('list_communautes')

#Permet au CM de bannir un utilisateur si ce dernier fait toujours parti de la communauté.
#On pourra le bannir à partir d'un POST ou d'un commentaire. Tous ses posts et commentaires seront supprimés.
def bannir(request, communaute_id, user_id):
    communaute = Communaute.objects.get(id=communaute_id)
    communaute.abonnes.remove(user_id)
    communaute.list_bannis.add(user_id)
    posts = Post.objects.filter(auteur_id=user_id)
    commentaires = Commentaire.objects.filter(auteur_id=user_id)
    for post in posts:
        post.delete()
    for commentaire in commentaires:
        commentaire.delete()
    return redirect('communaute', communaute_id=communaute_id)

# Renvoie l'ensemble des posts d'une communauté. Précisons le cas où la communauté est rendue invisible par
#l'admin : on ne pourrait plus avoir accès aux posts.
@login_required(login_url='/accounts/login/')
def communaute(request, communaute_id):
    communaute = Communaute.objects.get(id=communaute_id)
    if not Communaute.objects.get(id=communaute_id).ferme_invisible:
        posts = Post.objects.filter(communaute_id=communaute_id)
        date_now = timezone.now()

        list_priorite = Priorite.objects.all()
        dft_priorite = list_priorite.get(rang=list_priorite.count())

        # Form pour filtrer les posts affiches
        form_filtrage = FiltragePostCommunauteForm(request.POST or None)
        if form_filtrage.is_valid():
            et = form_filtrage.cleaned_data['type_filtrage']
            min_priorite = form_filtrage.cleaned_data['min_priorite']
            que_evt = form_filtrage.cleaned_data['que_evt']
            if que_evt:
                if et == "ET":
                    posts = posts.filter(priorite__rang__lte=min_priorite.rang, evenementiel=que_evt)
                else:
                    posts = posts.filter(priorite__rang__lte=min_priorite.rang) | posts.filter(evenementiel=que_evt)
            else:
                posts = posts.filter(priorite__rang__lte=min_priorite.rang)
            filtre = True
        return render(request, 'communitymanager/communaute.html', locals())
    else:
        return redirect("list_communautes")



# Permet à l'utilisateur connecté de créer un commentaire. Il sera prérempli au niveau de la section Auteur,
# et POST.
@login_required(login_url='/accounts/login/')
def commentaire(request, post_id):
    date_now = timezone.now()
    post = Post.objects.get(id=post_id)
    commentaires = Commentaire.objects.filter(post_id=post_id)
    form = CommentaireForm(request.POST or None)

    if form.is_valid():
        commentaire = form.save(commit=False)
        commentaire.post = post
        commentaire.auteur = request.user
        commentaire.save()
        form = CommentaireForm()
        envoi = True

    # Le post est considéré comme lu quand l'utilisateur accède à cette vue
    post.lecteurs.add(request.user)
    post.save()

    return render(request, 'communitymanager/post.html', locals())

#Permet de rendre un commentaire visible ou non à l'ensemble des autres utilisateurs
def visibilite_commentaire(request, commentaire_id):
   commentaire = Commentaire.objects.get(id=commentaire_id)
   if commentaire.invisible:
       commentaire.invisible=False
       commentaire.save()
   else:
       commentaire.invisible = True
       commentaire.save()
   return redirect('post', post_id=commentaire.post_id)

# Permet à l'utilisateur connecté de créer un POST. Il sera prérempli au niveau de la section Auteur,
# et les choix de la communauté (lieu de publication) seront limités. L'utilisateur ne pourra poster que dans les
# communautés auxquelles il est abonné.

@login_required(login_url='/accounts/login/')
def nouveau_post(request):
    date_now = timezone.now().strftime("%Y-%m-%dT%H:%M")
    date_evnt = None

    list_priorite = Priorite.objects.all()      #recupère la liste des priorite disponible
    form = PostForm(
        request.POST or None, user=request.user)
    communautes = Communaute.objects.filter(abonnes=request.user, ferme=False, ferme_invisible=False)   #Liste des communautes accessibles par l'utilisateur
    form.fields['commu'].choices = [(communaute.id, communaute.name) for communaute in
                                         communautes]  # On limite la communauté où le POST sera partagé,
    # aux communautés auxquelles l'abonnée fait parti.
    if request.user.is_superuser:
        superuser=True
    else:
        superuser = False
    if form.is_valid():
        post_cree = form.save(user=request.user)
        post_cree.lecteurs.add(request.user)
        post_cree.save()
        envoi = True
        return redirect(communaute, communaute_id=post_cree.communaute.id)
    return render(request, 'communitymanager/nouveau_post.html', locals())


# Permet à l'utilisateur connecté de modifier son POST. La vue prend en compte l'auteur du post, et renvoie une erreur si
# l'utilisateur tente de modifier un POST dont il n'est pas l'auteur. Le paramètre alert_flag renvoie un booléen. Il est FALSE
# si la modification du POST est lancée par un autre utilisateur que l'auteur.
@login_required(login_url='/accounts/login/')
def modification_post(request, post_id):
    date_now = timezone.now().strftime("%Y-%m-%dT%H:%M")

    try:
        post = Post.objects.get(id=post_id)
    except Http404:
        redirect(nouveau_post)

    list_priorite = Priorite.objects.all()
    communautes = Communaute.objects.filter(abonnes=request.user, ferme=False, ferme_invisible=False)
    if post.auteur == request.user:
        alert_flag = False
        form = PostForm(request.POST or None, instance=post, user=request.user)
        form.fields['commu'].initial = post.communaute.name
        form.fields['date_evenement'].initial = post.date_evenement

        if form.is_valid():
            post = form.modifPost(id=post.id)
            envoi = True
            return redirect(communaute, communaute_id=post.communaute.id)
    else:
        alert_flag = True
    return render(request, 'communitymanager/update_post.html', locals())

#Permet de rendre un POST visible ou non à l'ensemble des autres utilisateurs
def visibilite_post(request, post_id):
   post = Post.objects.get(id=post_id)
   if post.visible:
       post.visible=False
       post.save()
   else:
       post.visible = True
       post.save()
   return redirect('communaute', communaute_id=post.communaute_id)

# Permet de renvoyer tous les POSTs dont l'utilisateur est l'auteur.
@login_required(login_url='/accounts/login/')
def voir_posts(request):
    posts = Post.objects.filter(auteur=request.user)
    date_now = timezone.now()
    return render(
        request,
        'communitymanager/see_posts.html',
        locals()
    )


# Vue permettant de créer une communauté, avec l'utilisateur comme auteur
@login_required(login_url='/accounts/login/')
def creation_communaute(request):
    communautes = Communaute.objects.all()
    form = CommunauteForm(
        request.POST or None)
    form.fields['createur'].choices = [
        (request.user.id, request.user.username)]
    if form.is_valid():
        form.save(commit=False)
        communaute = form.save()
        communaute.abonnes.add(request.user)
        envoi = True
        return redirect('list_communautes')
    return render(request, 'communitymanager/nouvelle_communaute.html', locals())


# Vue permettant de modifier une communauté que l'utilisateur a créée
@login_required(login_url='/accounts/login/')
def modification_communaute(request, communaute_id):
    date_now = timezone.now()
    communaute = Communaute.objects.get(id=communaute_id)
    alert_flag = True
    if communaute.createur == request.user:
        alert_flag = False
        form = ModificationCommunauteForm(request.POST or None, instance=communaute)
        if form.is_valid():
            communaute = form.save()
            communaute.save()
            envoi = True
    else:
        alert_flag = True
    return render(request, 'communitymanager/update_communaute.html', locals())

# Vue permettant de fermer une communauté que l'utilisateur a créée. Il n'y sera plus possible d'y publier des commentaires ou des posts
@login_required(login_url='/accounts/login/')
def fermer_communaute(request, communaute_id):
    communaute = Communaute.objects.get(id=communaute_id)
    if communaute.ferme:
        communaute.ferme = False
        communaute.save()
    else:
        communaute.ferme = True
        communaute.save()
    return redirect('list_communautes')

@login_required(login_url='/accounts/login/')
def fermer_invisible_communaute(request, communaute_id):
    communaute = Communaute.objects.get(id=communaute_id)
    if communaute.ferme_invisible:
        communaute.ferme_invisible = False
        communaute.save()
    else:
        communaute.ferme_invisible = True
        communaute.save()
    return redirect('list_communautes')

#Vue permettant de détruire une communauté que l'utilisateur a créée
@login_required(login_url='/accounts/login/')
def detruire_communaute(request, communaute_id):
    Communaute.objects.get(id=communaute_id).delete()
    return redirect('list_communautes')

#Vue permettant de supprimer un post d'une communauté
@login_required(login_url='/accounts/login/')
def supprimer_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect(communaute, communaute_id=post.communaute.id)


# Permet à l'utilisateur de liker/unliker un post
@login_required(login_url='/accounts/login/')
def liker(request, post_id):
    post = Post.objects.get(id=post_id)

    # Mise à jour de la liste des utilisateurs qui like le post
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect(reverse('post', args=[post_id])) # permettre de liker depuis la page de détail du post uniquement?