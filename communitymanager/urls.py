from django.urls import path, include

from . import views

urlpatterns = [
    path('list_communautes', views.liste_communautes, name="list_communautes"),
    path('abonnements/<int:communaute_id>', views.abonner, name="abonnements"),
    path('fermer/<int:communaute_id>', views.fermer_communaute, name="fermer"),
    path('communaute/<int:communaute_id>/', views.communaute, name="communaute"),
    path('communaute/post/<int:post_id>', views.commentaire, name="post"),
    path('communaute/nouveau_post/', views.nouveau_post, name="nouveau_post"),
    path('nouvelle_communaute/', views.creation_communaute, name="nouvelle_communaute"),
    path('communaute/update_post/<int:post_id>', views.modification_post, name="update_post"),
    path('see_posts', views.voir_posts, name="see_posts"),
    path('feed_abonnements', views.accueil, name="feed_abonnements"),

]
