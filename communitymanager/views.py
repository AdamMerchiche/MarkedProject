from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse


# Create your views here.

def communautes(request):
    communautes = Communaute.objects.all()
    for communaute in communautes:
        if (request.user in communaute.abonnes.all()):  # finir ca ici
            return render(request, 'communitymanager/communautes.html', {'communaute_abo': communautes})
        else:
            return render(request, 'communitymanager/communautes.html', {'communaute_abo': communautes})


def list_communautes(request):
    communautes = Communaute.objects.all()
    return render(request, 'communitymanager/list_communautes.html', {'communaute': communautes})


def statut(request):
    communautes = Communaute.objects.all()
    is_abonne = False
    for communaute in communautes:
        print(communaute)
        if request.user in communaute.abonnes.all():
            print(communaute.abonnes.all())
            is_abonne = False
            communaute.abonnes == communaute.abonnes.exclude(username=request.user)
        else:
            is_abonne = True
            print(communaute.abonnes.all())
            communaute.abonnes.all() == communaute.abonnes.add(request.user)
            communaute.abonnes.all().save()
    return render(request, 'communitymanager/abonnement.html', {'communautes': communautes, 'is_abonne': is_abonne})
