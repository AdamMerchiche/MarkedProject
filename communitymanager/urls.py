from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('list_communautes', views.list_communautes, name="list_communautes"),
    path('abonnements', views.statut, name="abonnements"),
    path('communaute/<int:communaute_id>/', views.communaute, name="communaute")
]
