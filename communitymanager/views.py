from .forms import *
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required


# Renvoie le feed d'un utilisateur, avec tous les posts des communautés auxquelles il est abonné
@login_required
def accueil(request):
    communautes = Communaute.objects.filter(abonnes=request.user)
    posts = Post.objects.filter(communaute__abonnes=request.user)
    return render(request, 'communitymanager/feed_abonnements.html', locals())


# Renvoie la liste de toutes les communautés
@login_required
def liste_communautes(request):
    communautes = Communaute.objects.all()
    return render(request, 'communitymanager/list_communautes.html', {'communautes': communautes})


# Permet à l'utilisateur de s'abonner ou se désabonner d'une communauté
@login_required
def abonner(request, communaute_id):
    communaute = Communaute.objects.get(id=communaute_id)
    if request.user in communaute.abonnes.all():
        communaute.abonnes.remove(request.user)
    else:
        communaute.abonnes.add(request.user)
    return redirect('list_communautes')


# Renvoie l'ensemble des posts d'une communauté précise
@login_required
def communaute(request, communaute_id):
    return render(request, 'communitymanager/communaute.html',
                  {'posts': Post.objects.filter(communaute_id=communaute_id)})


# Permet à l'utilisateur connecté de créer un commentaire. Il sera prérempli au niveau de la section Auteur,
# et POST.
@login_required
def commentaire(request, post_id):
    post = Post.objects.get(id=post_id)
    commentaires = Commentaire.objects.filter(post_id=post_id)
    form = CommentaireForm(request.POST or None)
    form.fields['auteur'].choices = [
        (request.user.id, request.user.username)]  # On limite le choix de l'auteur à l'utilisateur uniquement.
    # On ne peut de fait, pas créer de post si l'authentification n'est pas faite.
    form.fields['post'].choices = [(post_id,
                                    post.title)]  # On limite le choix du POST que l'abonné commente.
    # Il ne peut commenter que le POST sur lequel il se trouve.

    if form.is_valid():
        commentaire = form.save()
        commentaire.post_id = post_id
        commentaire.auteur_id = request.user.id
        commentaire.save()
        envoi = True
    return render(request, 'communitymanager/post.html', locals())


# Permet à l'utilisateur connecté de créer un POST. Il sera prérempli au niveau de la section Auteur,
# et les choix de la communauté (lieu de publication) seront limités. L'utilisateur ne pourra poster que dans les
# communautés auxquelles il est abonné.
@login_required
def nouveau_post(request):
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
        form.save()
        envoi = True
    return render(request, 'communitymanager/nouveau_post.html', locals())


# Permet à l'utilisateur connecté de modifier son POST. La vue prend en compte l'auteur du post, et renvoie une erreur si
# l'utilisateur tente de modifier un POST dont il n'est pas l'auteur. Le paramètre alert_flag renvoie un booléen. Il est FALSE
# si la modification du POST est lancée par un autre utilisateur que l'auteur.
@login_required
def modification_post(request, post_id):
    post = Post.objects.get(id=post_id)
    alert_flag = True
    if post.auteur == request.user:
        alert_flag = False
        form = ModificationPostForm(request.POST or None, instance=post)
        if form.is_valid():
            post = form.save()
            post.save()
            envoi = True

    else:
        alert_flag = True
    return render(request, 'communitymanager/update_post.html', locals())


# Permet de renvoyer tous les POSTs dont l'utilisateur est l'auteur.
@login_required
def voir_posts(request):
    return render(
        request,
        'communitymanager/see_posts.html',
        {"posts": Post.objects.filter(auteur=request.user)}
    )
