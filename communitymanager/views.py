from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required


# Renvoie le feed d'un utilisateur, avec tous les posts des communautés auxquelles il est abonné
@login_required(login_url='/accounts/login/')
def accueil(request):
    date_now = timezone.now()

    communautes = Communaute.objects.filter(abonnes=request.user)
    posts = Post.objects.filter(communaute__abonnes=request.user)
    posts = [(post, post.lecteurs.filter(id=request.user.id).exists()) for post in posts]
    return render(request, 'communitymanager/feed_abonnements.html', locals())


# Renvoie la liste de toutes les communautés
@login_required(login_url='/accounts/login/')
def liste_communautes(request):
    date_now = timezone.now()

    communautes = Communaute.objects.all()
    return render(request, 'communitymanager/list_communautes.html', {'communautes': communautes})


# Permet à l'utilisateur de s'abonner ou se désabonner d'une communauté
@login_required(login_url='/accounts/login/')
def abonner(request, communaute_id):
    date_now = timezone.now()

    communaute = Communaute.objects.get(id=communaute_id)
    if request.user in communaute.abonnes.all():
        communaute.abonnes.remove(request.user)
    else:
        communaute.abonnes.add(request.user)
    return redirect('list_communautes')


# Renvoie l'ensemble des posts d'une communauté précise
@login_required(login_url='/accounts/login/')
def communaute(request, communaute_id):
    posts = Post.objects.filter(communaute_id=communaute_id)
    date_now = timezone.now()
    posts = [(post, post.lecteurs.filter(id=request.user.id).exists()) for post in posts]

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


# Permet à l'utilisateur connecté de créer un POST. Il sera prérempli au niveau de la section Auteur,
# et les choix de la communauté (lieu de publication) seront limités. L'utilisateur ne pourra poster que dans les
# communautés auxquelles il est abonné.
@login_required(login_url='/accounts/login/')
def nouveau_post(request):
    date_now = timezone.now()

    form = PostForm(
        request.POST or None)
    communautes = Communaute.objects.filter(abonnes=request.user)
    form.fields['auteur'].choices = [
        (request.user.id, request.user.username)]  # On limite le choix de l'auteur à l'utilisateur uniquement.
    # On ne peut de fait, pas créer de post si l'authentification n'est pas faite.
    form.fields['communaute'].choices = [(communaute.id, communaute.name) for communaute in
                                         communautes]  # On limite la communauté où le POST sera partagé,
    # aux communautés auxquelles l'abonnée fait parti.
    if form.is_valid():
        post_cree = form.save()
        envoi = True
        return redirect(commentaire, post_id=post_cree.id)
    return render(request, 'communitymanager/nouveau_post.html', locals())


# Permet à l'utilisateur connecté de modifier son POST. La vue prend en compte l'auteur du post, et renvoie une erreur si
# l'utilisateur tente de modifier un POST dont il n'est pas l'auteur. Le paramètre alert_flag renvoie un booléen. Il est FALSE
# si la modification du POST est lancée par un autre utilisateur que l'auteur.
@login_required(login_url='/accounts/login/')
def modification_post(request, post_id):
    date_now = timezone.now()

    post = Post.objects.get(id=post_id)
    alert_flag = True
    if post.auteur == request.user:
        alert_flag = False
        form = ModificationPostForm(request.POST or None, instance=post)
        if form.is_valid():
            post = form.save()
            post.save()
            envoi = True
            return redirect(commentaire, post_id=post.id)
    else:
        alert_flag = True
    return render(request, 'communitymanager/update_post.html', locals())


# Permet de renvoyer tous les POSTs dont l'utilisateur est l'auteur.
@login_required(login_url='/accounts/login/')
def voir_posts(request):
    posts = Post.objects.filter(auteur=request.user)
    posts = [(post, post.lecteurs.filter(id=request.user.id).exists()) for post in posts]
    return render(
        request,
        'communitymanager/see_posts.html',
        {"posts": posts,"date_now":timezone.now()}
    )


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