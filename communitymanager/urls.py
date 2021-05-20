from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('communautes', views.communautes, name="communautes"),
    path('abonnements', views.statut, name="abonnements"),
]
