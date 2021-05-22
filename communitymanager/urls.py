from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('list_communautes', views.list_communautes, name="list_communautes"),
    path('abonnements', views.statut, name="abonnements"),
    path('communaute/<int:communaute_id>/', views.communaute, name="communaute"),
    path('communaute/post/<int:post_id>', views.post, name="post"),
    path('communaute/post/nouveau_commentaire', views.nouveau_commentaire, name="nouveau_commentaire"),

]
