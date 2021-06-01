from .forms import *
from django.shortcuts import render, redirect
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
    return render(request, 'communitymanager/communaute.html',
                  {'posts': Post.objects.filter(communaute_id=communaute_id),"date_now":timezone.now()})


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
    return render(request, 'communitymanager/post.html', locals())


# Permet à l'utilisateur connecté de créer un POST. Il sera prérempli au niveau de la section Auteur,
# et les choix de la communauté (lieu de publication) seront limités. L'utilisateur ne pourra poster que dans les
# communautés auxquelles il est abonné.
@login_required(login_url='/accounts/login/')
def nouveau_post(request):
    date_now = timezone.now().strftime("%Y-%m-%dT%H:%M")
    date_evnt = None

    list_priorite = Priorite.objects.all()
    form = PostForm(request.POST or None)
    communautes = Communaute.objects.filter(abonnes=request.user)

    if form.is_valid():
        post_cree = form.save(user=request.user)
        envoi = True
        return redirect(commentaire, post_id=post_cree.id)
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
    communautes = Communaute.objects.filter(abonnes=request.user)
    alert_flag = True
    if post.auteur == request.user:
        alert_flag = False
        form = PostForm(request.POST or None, instance=post)
        form.fields['commu'].initial = post.communaute.name
        form.fields['date_evenement'].initial = post.date_evenement

        if form.is_valid():
            post = form.modifPost(id=post.id)
            envoi = True
            return redirect(commentaire, post_id=post.id)
    else:
        alert_flag = True
    return render(request, 'communitymanager/update_post.html', locals())


# Permet de renvoyer tous les POSTs dont l'utilisateur est l'auteur.
@login_required(login_url='/accounts/login/')
def voir_posts(request):
    return render(
        request,
        'communitymanager/see_posts.html',
        {"posts": Post.objects.filter(auteur=request.user),"date_now":timezone.now()}
    )
