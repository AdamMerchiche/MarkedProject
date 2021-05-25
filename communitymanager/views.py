from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from .models import*
from django.contrib.auth.decorators import login_required




@login_required
def home(request):
    communautes = Communaute.objects.filter(abonnes=request.user)
    posts = Post.objects.filter(communaute__abonnes=request.user)
    return render(request, 'communitymanager/feed_abonnements.html', locals())

@login_required
def list_communautes(request):
    communautes = Communaute.objects.all()
    return render(request, 'communitymanager/list_communautes.html', {'communautes': communautes})


@login_required
def statut(request, communaute_id):
    communaute = Communaute.objects.get(id=communaute_id)
    if request.user in communaute.abonnes.all():
        communaute.abonnes.remove(request.user)
    else:
        communaute.abonnes.add(request.user)
    return redirect ('list_communautes')

@login_required
def list_abonnements(request):
    return render(request, 'communitymanager/feed_abonnements.html', {'communautes': Communaute.objects.filter(abonnes= request.user)})


def communaute(request, communaute_id):
    return render(request, 'communitymanager/communaute.html', {'posts': Post.objects.filter(communaute_id= communaute_id)})
@login_required
def post(request, post_id):
    post=Post.objects.get(id=post_id)
    commentaires = Commentaire.objects.filter(post_id = post_id)
    form = CommentaireForm(request.POST or None)
    form.fields['auteur'].choices = [(request.user.id, request.user.username)]
    form.fields['post'].choices = [(post_id, post.title)]

    if form.is_valid():
        commentaire = form.save()
        commentaire.post_id=post_id
        commentaire.auteur_id=request.user.id
        commentaire.save()
        envoi = True
    return render(request, 'communitymanager/post.html', locals())

@login_required
def nouveau_commentaire(request):
    form = CommentaireForm(
        request.POST or None)
    form.fields['auteur'].choices = [(request.user.id, request.user.username)]
    if form.is_valid():
        form.save()
        envoi = True
    return render(request, 'communitymanager/post.html', locals())

@login_required
def nouveau_post(request):
    form = PostForm(
        request.POST or None)
    communautes = Communaute.objects.filter(abonnes=request.user)
    form.fields['auteur'].choices = [(request.user.id, request.user.username)]
    form.fields['communaute'].choices = [(communaute.id, communaute.name) for communaute in communautes]
    if form.is_valid():
        form.save()
        envoi = True
    return render(request, 'communitymanager/nouveau_post.html', locals())

@login_required
def update_post(request, post_id):
    post = Post.objects.get(id=post_id) #Corriger ici, y'a un problème, quand on
    # modifie un article ca modifie tou s les articles de l'auteur
    if post.auteur == request.user:
        form = UpdateForm(request.POST or None, instance=post)
        if form.is_valid():
            post = form.save()
            post.save()
            envoi = True
    else:
        return HttpResponse("Vous n'êtes pas l'auteur de ce POST. Vous ne pouvez donc pas le modifier. ")
    return render(request, 'communitymanager/update_post.html', locals())

@login_required
def see_posts(request): ##ici je retourne tous les posts que l'auteur a écrit.
    #une fois que j'aurai compris comment prendre en compte l'abonnement, je mettrai tous les posts des communautés abonnées de l'utilisateur.
    return render(
        request,
        'communitymanager/see_posts.html',
        {"posts": Post.objects.filter(auteur=request.user)}
    )





"""def statut(request):
    communautes = Communaute.objects.all()
    is_abonne = False
    for communaute in communautes:
        if request.user in communaute.abonnes.all():
            is_abonne = False
        if not request.user in communaute.abonnes.all():
            is_abonne = True
        print(is_abonne)
    return render(request, 'communitymanager/abonnement.html', {'communautes': communautes,'is_abonne':is_abonne})"""


