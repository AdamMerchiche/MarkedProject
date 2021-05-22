from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from .models import*
from django.contrib.auth.decorators import login_required




# Create your views here.


def list_communautes(request):
    communautes = Communaute.objects.all()
    return render(request, 'communitymanager/list_communautes.html', {'communautes': communautes})

def statut(request):
    communautes = Communaute.objects.all()
    is_subd = False
    for communaute in communautes:
        if communaute.abonnes.filter(username=request.user).exists():
            communaute.abonnes.remove(request.user)
            is_subd = False
        else:
            communaute.abonnes.add(request.user)
            is_subd = True
    return render(request, 'communitymanager/abonnement.html', {'communautes': communautes,'is_subd':is_subd})

def communaute(request, communaute_id):
    return render(request, 'communitymanager/communaute.html', {'posts': Post.objects.filter(communaute_id= communaute_id)})

def post(request, post_id):
    return render(request, 'communitymanager/post.html', {'commentaires': Commentaire.objects.filter(post_id= post_id)})

def nouveau_commentaire(request):
    form = CommentaireForm(
        request.POST)
    if form.is_valid():
        form.save()
        envoi = True
    return render(request, 'communitymanager/nouveau_commentaire.html', locals())

def nouveau_post(request):
    form = PostForm(
        request.POST)
    if form.is_valid():
        form.save()
        envoi = True
    return render(request, 'communitymanager/nouveau_post.html', locals())

@login_required
def update_post(request):
    posts = Post.objects.filter(auteur_id =request.user.id)
    for post in posts :
        form = UpdateForm(
            request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            envoi = True
    return render(request, 'communitymanager/update_post.html', locals())






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


