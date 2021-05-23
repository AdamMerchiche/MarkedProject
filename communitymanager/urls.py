from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('list_communautes', views.list_communautes, name="list_communautes"),
    path('abonnements/<int:communaute_id>', views.statut, name="abonnements"),
    path('communaute/<int:communaute_id>/', views.communaute, name="communaute"),
    path('communaute/post/<int:post_id>', views.post, name="post"),
    path('communaute/post/nouveau_commentaire', views.nouveau_commentaire, name="nouveau_commentaire"),
    path('communaute/nouveau_post', views.nouveau_post, name="nouveau_post"),
    path('communaute/update_post/<int:post_id>', views.update_post, name="update_post"),
    path('see_posts', views.see_posts, name="see_posts"),
    path('list_abonnements', views.list_abonnements, name="list_abonnements"),

]
