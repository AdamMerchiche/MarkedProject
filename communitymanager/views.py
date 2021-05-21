from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse



# Create your views here.

def communautes(request):
    communautes = Communaute.objects.all() # finir ca ici
    return render(request, 'communitymanager/communautes.html', {'communaute_abo': communautes})



def list_communautes(request):
    communautes = Communaute.objects.all()
    return render(request, 'communitymanager/list_communautes.html', {'communaute': communautes})

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


