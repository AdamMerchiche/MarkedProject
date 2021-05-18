from django.contrib.auth import authenticate, login
from .forms import*
from django.contrib.auth import logout
from django.shortcuts import render, redirect

# Create your views here.
"""def deconnexion(request):
    logout(request)
    return redirect(reverse(connexion))



def connexion(request):
    error = False
    if request.method =="POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password"]
            user = authenticate(username=username, password=password) #on check si les données sont bien correctes pour l'utilisateur

            if user:
                login(request, user)
            else:
                error=True
        else:
            form=ConnexionForm()
    return render(request, 'communitymanager/connexion.html', locals())"""


