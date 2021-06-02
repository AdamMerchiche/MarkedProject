from django.urls import path, include

from . import views

urlpatterns = [
    path('list_communautes', views.liste_communautes, name="list_communautes"),
    path('abonnements/<int:communaute_id>', views.abonner, name="abonnements"),
    path('fermer/<int:communaute_id>', views.fermer_communaute, name="fermer"),
    path('fermer_invisible/<int:communaute_id>', views.fermer_invisible_communaute, name="fermer_invisible"),
    path('fermer/<int:communaute_id>/<int:user_id>', views.bannir, name="bannir"),
    path('detruire/<int:communaute_id>', views.detruire_communaute, name="detruire"),
    path('communaute/<int:communaute_id>/', views.communaute, name="communaute"),
    path('communaute/post/<int:post_id>', views.commentaire, name="post"),
    path('communaute/nouveau_post/', views.nouveau_post, name="nouveau_post"),
    path('nouvelle_communaute/', views.creation_communaute, name="nouvelle_communaute"),
    path('communaute/update_post/<int:post_id>', views.modification_post, name="update_post"),
    path('communaute/visibilité_commentaire/<int:commentaire_id>', views.visibilite_commentaire, name="visibilite_commentaire"),
    path('communaute/visibilité_post/<int:post_id>', views.visibilite_post,
         name="visibilite_post"),
    path('communaute/supprimer_post/<int:post_id>', views.supprimer_post,
         name="supprimer_post"),
    path('communaute/update_communaute/<int:communaute_id>', views.modification_communaute, name="update_communaute"),
    path('see_posts', views.voir_posts, name="see_posts"),
    path('feed_abonnements', views.accueil, name="feed_abonnements"),
    path('like/post/<int:post_id>', views.liker, name="liker"),
]
