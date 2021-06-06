from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q


# Renvoie le feed d'un utilisateur, avec tous les posts des communautés auxquelles il est abonné
@login_required()
def accueil(request):
    date_now = timezone.now()

    communautes = Communaute.objects.filter(abonnes=request.user)
    initial_list = Post.objects.filter(
        communaute__abonnes=request.user)  # 2 listes differentes posts et initial posts pour des raisons d'affichages
    posts = initial_list
    # Formulaire pour afficher une liste de post contenant une chaine de caractères
    search = SimpleSearchForm(request.POST or None, prefix='local_search')
    action_url = reverse('feed_abonnements')
    if search.is_valid():
        query = search.cleaned_data['simple_query']
        posts = initial_list.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query))

    # Block du formulaire de recherche global renvoyant vers la page de recherche preremplie
    action_large_search = reverse('feed_abonnements')
    large_search = SimpleSearchForm(request.POST or None, prefix='large_search')
    if large_search.is_valid():
        large_query = large_search.cleaned_data['simple_query']
        request.session["large_query"] = large_query
        return redirect('recherche')
    return render(request, 'communitymanager/feed_abonnements.html', locals())


# Renvoie la liste de toutes les communautés
@login_required()
def liste_communautes(request):
    date_now = timezone.now()
    initial_list = Communaute.objects.all()  # 2 listes differentes posts et initial posts pour des raisons d'affichages
    communautes = initial_list
    # Gestion form pour chercher une communaute precise
    search = SimpleSearchForm(request.POST or None, prefix='local_search')
    action_url = reverse('list_communautes')  # Variable pour le template "search_form.html"
    if search.is_valid():
        query = search.cleaned_data['simple_query']
        communautes = initial_list.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query))

    nb_posts_non_lus = []
    for i in range(len(communautes)):
        if request.user == communautes[i].createur:
            nb_posts_non_lus.append(Post.objects.filter(communaute=communautes[i]).exclude(
                lecteurs__username=request.user.username).count())
        else:
            nb_posts_non_lus.append(Post.objects.filter(communaute=communautes[i], visible=True).exclude(
                lecteurs__username=request.user.username).count())
    communautes = [(communautes[i], nb_posts_non_lus[i]) for i in range(len(communautes))]

    # Block du formulaire de recherche global renvoyant vers la page de recherche preremplie
    action_large_search = reverse('feed_abonnements')
    large_search = SimpleSearchForm(request.POST or None, prefix='large_search')
    if large_search.is_valid():
        large_query = large_search.cleaned_data['simple_query']
        request.session["large_query"] = large_query
        return redirect('recherche')

    return render(request, 'communitymanager/list_communautes.html', locals())


# Permet à l'utilisateur de s'abonner ou se désabonner d'une communauté
@login_required()
def abonner(request, communaute_id):
    date_now = timezone.now()

    communaute = Communaute.objects.get(id=communaute_id)
    if request.user in communaute.abonnes.all():
        communaute.abonnes.remove(request.user)
    else:
        if not request.user in communaute.list_bannis.all():
            communaute.abonnes.add(request.user)
    return redirect('list_communautes')


# Permet au CM de bannir un utilisateur si ce dernier fait toujours parti de la communauté.
# On pourra le bannir à partir d'un POST ou d'un commentaire. Tous ses posts et commentaires seront supprimés.
@login_required()
def bannir(request, communaute_id, user_id):
    communaute = Communaute.objects.get(id=communaute_id)
    communaute.abonnes.remove(user_id)
    communaute.list_bannis.add(user_id)
    posts = Post.objects.filter(auteur_id=user_id)
    commentaires = Commentaire.objects.filter(auteur_id=user_id)
    for post in posts:
        post.delete()
    for commentaire in commentaires:
        commentaire.delete()
    return redirect('communaute', communaute_id=communaute_id)


# Renvoie l'ensemble des posts d'une communauté. Précisons le cas où la communauté est rendue invisible par
# l'admin : on ne pourrait plus avoir accès aux posts.
@login_required()
def communaute(request, communaute_id):
    communaute = Communaute.objects.get(id=communaute_id)
    # vérification que l'utilisateur est bien abonné pour pouvoir voir les post pour éviter de forcer l'acces avec l'url
    if request.user not in communaute.abonnes.all():
        return redirect('list_communautes')

    elif not Communaute.objects.get(id=communaute_id).ferme_invisible:
        date_now = timezone.now()
        posts = Post.objects.filter(communaute_id=communaute_id)
        # Données et form pour recherche générale
        action_large_search = reverse('feed_abonnements')
        large_search = SimpleSearchForm(request.POST or None, prefix='large_search')
        # Données et form pour recherche des posts de la communauté par chaîne de charactères
        initial_list = Post.objects.filter(communaute_id=communaute_id)
        search = SimpleSearchForm(request.POST or None, prefix='local_search')
        action_url = reverse('communaute', args=[communaute_id])
        # Données et form pour filtrage des posts de la communautés par priorités et événementiel
        list_priorite = Priorite.objects.all()
        dft_priorite = list_priorite.get(rang=list_priorite.count())
        form_filtrage = FiltragePostCommunauteForm(request.POST or None)

        # Form pour filtrer les posts affiches par priorites et evenementiel
        if form_filtrage.is_valid():
            et = form_filtrage.cleaned_data['type_filtrage']
            min_priorite = form_filtrage.cleaned_data['min_priorite']
            que_evt = form_filtrage.cleaned_data['que_evt']
            if que_evt:
                if et == "ET":
                    posts = posts.filter(priorite__rang__lte=min_priorite.rang, evenementiel=que_evt)
                else:
                    posts = posts.filter(priorite__rang__lte=min_priorite.rang) | posts.filter(evenementiel=que_evt)
            else:
                posts = posts.filter(priorite__rang__lte=min_priorite.rang)
            filtre = True
            return render(request, 'communitymanager/communaute.html', locals())

        posts = initial_list
        # Formulaire pour afficher une liste de post contenant une chaine de caractères
        if search.is_valid():
            query = search.cleaned_data['simple_query']
            posts = initial_list.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query))
            return render(request, 'communitymanager/communaute.html', locals())

        # Block du formulaire de recherche global renvoyant vers la page de recherche preremplie
        if large_search.is_valid():
            large_query = large_search.cleaned_data['simple_query']
            request.session["large_query"] = large_query
            return redirect('recherche')

        return render(request, 'communitymanager/communaute.html', locals())
    else:
        return redirect("list_communautes")


# Permet à l'utilisateur connecté de créer un commentaire. Il sera prérempli au niveau de la section Auteur,
# et POST.
@login_required()
def commentaire(request, post_id):
    date_now = timezone.now()
    post = Post.objects.get(id=post_id)
    if request.user not in post.communaute.abonnes.all():
        return redirect('list_communautes')
    commentaires = Commentaire.objects.filter(post_id=post_id)

    # Gestion formulaire de commentaire
    form = CommentaireForm(request.POST or None)
    if form.is_valid():
        commentaire = form.save(commit=False)
        commentaire.post = post
        commentaire.auteur = request.user
        commentaire.save()
        form = CommentaireForm()
        envoi = True

    # Le post est considéré comme lu quand l'utilisateur accède à cette vue
    post.lecteurs.add(request.user)
    post.save()

    # Block du formulaire de recherche global renvoyant vers la page de recherche preremplie
    action_large_search = reverse('feed_abonnements')
    large_search = SimpleSearchForm(request.POST or None, prefix='large_search')
    if large_search.is_valid():
        large_query = large_search.cleaned_data['simple_query']
        request.session["large_query"] = large_query
        return redirect('recherche')

    return render(request, 'communitymanager/post.html', locals())


# Permet de rendre un commentaire visible ou non à l'ensemble des autres utilisateurs
@login_required()
def visibilite_commentaire(request, commentaire_id):
    commentaire = Commentaire.objects.get(id=commentaire_id)
    if commentaire.invisible:
        commentaire.invisible = False
        commentaire.save()
    else:
        commentaire.invisible = True
        commentaire.save()
    return redirect('post', post_id=commentaire.post_id)


# Permet à l'utilisateur connecté de créer un POST. Il sera prérempli au niveau de la section Auteur,
# et les choix de la communauté (lieu de publication) seront limités. L'utilisateur ne pourra poster que dans les
# communautés auxquelles il est abonné.
@login_required()
def nouveau_post(request):
    date_now = timezone.now().strftime("%Y-%m-%dT%H:%M")
    date_evnt = None

    list_priorite = Priorite.objects.all()  # recupère la liste des priorite disponible
    form = PostForm(
        request.POST or None, user=request.user)
    communautes = Communaute.objects.filter(abonnes=request.user, ferme=False,
                                            ferme_invisible=False)  # Liste des communautes accessibles par l'utilisateur
    form.fields['commu'].choices = [(communaute.id, communaute.name) for communaute in
                                    communautes]  # On limite la communauté où le POST sera partagé,
    # aux communautés auxquelles l'abonnée fait parti.
    if request.user.is_superuser:
        superuser = True
    else:
        superuser = False
    if form.is_valid():
        post_cree = form.save(user=request.user)
        post_cree.lecteurs.add(request.user)
        post_cree.save()
        envoi = True
        return redirect('communaute', communaute_id=post_cree.communaute.id)

    # Block du formulaire de recherche global renvoyant vers la page de recherche preremplie
    action_large_search = reverse('feed_abonnements')
    large_search = SimpleSearchForm(request.POST or None, prefix='large_search')
    if large_search.is_valid():
        large_query = large_search.cleaned_data['simple_query']
        request.session["large_query"] = large_query
        return redirect('recherche')

    return render(request, 'communitymanager/nouveau_post.html', locals())


# Permet à l'utilisateur connecté de modifier son POST. La vue prend en compte l'auteur du post, et renvoie une erreur si
# l'utilisateur tente de modifier un POST dont il n'est pas l'auteur. Le paramètre alert_flag renvoie un booléen. Il est FALSE
# si la modification du POST est lancée par un autre utilisateur que l'auteur.
@login_required()
def modification_post(request, post_id):
    date_now = timezone.now().strftime(
        "%Y-%m-%dT%H:%M")  # date minimale pour un evenement, cad au moment du post. On ne peut pas mettre un evnt au passé.

    # Block du formulaire de recherche global renvoyant vers la page de recherche preremplie
    action_large_search = reverse('feed_abonnements')
    large_search = SimpleSearchForm(request.POST or None, prefix='large_search')
    if large_search.is_valid():
        large_query = large_search.cleaned_data['simple_query']
        request.session["large_query"] = large_query
        return redirect('recherche')

    try:
        post = Post.objects.get(id=post_id)
    except Http404:
        return redirect(nouveau_post)

    list_priorite = Priorite.objects.all()
    communautes = Communaute.objects.filter(abonnes=request.user, ferme=False, ferme_invisible=False)
    if post.auteur == request.user:
        alert_flag = False
        form = PostForm(request.POST or None, instance=post, user=request.user)
        form.fields['commu'].initial = post.communaute.name
        form.fields['date_evenement'].initial = post.date_evenement

        if form.is_valid():
            post = form.modifPost(id=post.id)
            envoi = True
            return redirect(communaute, communaute_id=post.communaute.id)
    else:
        alert_flag = True
    return render(request, 'communitymanager/update_post.html', locals())


# Permet de rendre un POST visible ou non à l'ensemble des autres utilisateurs
@login_required()
def visibilite_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.visible:
        post.visible = False
        post.save()
    else:
        post.visible = True
        post.save()
    return redirect('communaute', communaute_id=post.communaute_id)


# Permet de renvoyer tous les POSTs dont l'utilisateur est l'auteur.
@login_required()
def voir_posts(request):
    initial_list = Post.objects.filter(auteur=request.user)
    posts = initial_list
    # Formulaire pour afficher une liste de post contenant une chaine de caractères
    search = SimpleSearchForm(request.POST or None, prefix='local_search')
    action_url = reverse('feed_abonnements')
    if search.is_valid():
        query = search.cleaned_data['simple_query']
        posts = initial_list.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query))

    date_now = timezone.now()

    # Block du formulaire de recherche global renvoyant vers la page de recherche preremplie
    action_large_search = reverse('feed_abonnements')
    large_search = SimpleSearchForm(request.POST or None, prefix='large_search')
    if large_search.is_valid():
        large_query = large_search.cleaned_data['simple_query']
        request.session["large_query"] = large_query
        return redirect('recherche')
    return render(request, 'communitymanager/see_posts.html', locals())


# Vue permettant de créer une communauté, avec l'utilisateur comme auteur
@login_required()
def creation_communaute(request):
    communautes = Communaute.objects.all()
    form = CommunauteForm(
        request.POST or None)
    form.fields['list_CMs'].initial = request.user
    if form.is_valid():
        form.save(user=request.user)
        communaute = form.save(user=request.user)
        # Le créateur est directement abonné et ajouté à la liste des CMs
        communaute.abonnes.add(request.user)
        communaute.list_CMs.add(request.user)
        envoi = True
        return redirect('list_communautes')

    # Block du formulaire de recherche global renvoyant vers la page de recherche preremplie
    action_large_search = reverse('feed_abonnements')
    large_search = SimpleSearchForm(request.POST or None, prefix='large_search')
    if large_search.is_valid():
        large_query = large_search.cleaned_data['simple_query']
        request.session["large_query"] = large_query
        return redirect('recherche')
    return render(request, 'communitymanager/nouvelle_communaute.html', locals())


# Vue permettant d'ajouter ou supprimer un CM d'une communauté.
@login_required()
def ajouter_CM(request, user_id, communaute_id):
    communaute = Communaute.objects.get(id=communaute_id)
    if communaute.list_CMs.filter(id=user_id).exists():
        communaute.list_CMs.remove(user_id)
    else:
        communaute.list_CMs.add(user_id)
    return redirect('list_communautes')


# Vue permettant de modifier une communauté que l'utilisateur a créée
@login_required()
def modification_communaute(request, communaute_id):
    # Block du formulaire de recherche global renvoyant vers la page de recherche preremplie
    action_large_search = reverse('feed_abonnements')
    large_search = SimpleSearchForm(request.POST or None, prefix='large_search')
    if large_search.is_valid():
        large_query = large_search.cleaned_data['simple_query']
        request.session["large_query"] = large_query
        return redirect('recherche')

    try:
        communaute = Communaute.objects.get(id=communaute_id)
    except Http404:
        return redirect(liste_communautes)
    alert_flag = True
    # La modification de la communauté est impossible si l'utilisateur n'est pas CM
    if request.user in communaute.list_CMs.all():
        alert_flag = False
        form = ModificationCommunauteForm(request.POST or None, instance=communaute)
        if form.is_valid():
            communaute = form.save()
            envoi = True
            return redirect(liste_communautes)
    else:
        alert_flag = True
    return render(request, 'communitymanager/update_communaute.html', locals())


# Vue permettant de fermer une communauté que l'utilisateur a créée. Il n'y sera plus possible d'y publier des commentaires ou des posts
@login_required()
def fermer_communaute(request, communaute_id):
    communaute = Communaute.objects.get(id=communaute_id)
    if communaute.ferme:
        communaute.ferme = False
        communaute.save()
    else:
        communaute.ferme = True
        communaute.save()
    return redirect('list_communautes')


# Vue permettant de totalement bloquer une communauté. Aucun accès aux données internes
@login_required()
def fermer_invisible_communaute(request, communaute_id):
    communaute = Communaute.objects.get(id=communaute_id)
    if communaute.ferme_invisible:
        communaute.ferme_invisible = False
        communaute.save()
    else:
        communaute.ferme_invisible = True
        communaute.save()
    return redirect('list_communautes')


# Vue permettant de détruire une communauté que l'utilisateur a créée
@login_required()
def detruire_communaute(request, communaute_id):
    Communaute.objects.get(id=communaute_id).delete()
    return redirect('list_communautes')


# Vue permettant de supprimer un post d'une communauté
@login_required()
def supprimer_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('communaute', communaute_id=post.communaute.id)


# Permet à l'utilisateur de liker/unliker un post
@login_required()
def liker(request, post_id):
    post = Post.objects.get(id=post_id)

    # Mise à jour de la liste des utilisateurs qui like le post
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect(reverse('post', args=[post_id]))


# Permet à l'utilisateur de faire une recherche
@login_required()
def recherche(request):
    date_now = timezone.now()

    # Block du formulaire de recherche global renvoyant vers la page de recherche preremplie
    action_large_search = reverse('feed_abonnements')
    large_search = SimpleSearchForm(request.POST or None, prefix='large_search')
    if large_search.is_valid():
        large_query = large_search.cleaned_data['simple_query']
        request.session["large_query"] = large_query
        return redirect('recherche')

    try:
        large_query = request.session.get('large_query')
        search_form_dict = {'query': large_query}
        communautes, posts, communautes_par_createur, posts_par_auteur = resultats_recherche(search_form_dict, request)
    except:
        redirect('feed_abonnements')  # permet de bloquerl'accès forcé par l'url

    advanced_search = SearchForm(request.POST or None)
    advanced_search.fields['query'].initial = large_query
    if advanced_search.is_valid():
        search_form_dict = SearchForm.cleaned_data

    communautes, posts, communautes_par_createur, posts_par_auteur = resultats_recherche(request, search_form_dict)
    return render(request, 'communitymanager/recherche.html', locals())


# Fonction de traitement de la recherche pour alleger la vue
@login_required()
def resultats_recherche(request, form_field):
    # Traitement de la recherche
    large_query = form_field['query']

    # Recherche dans les communautes
    communautes = Communaute.objects.filter(
        Q(name__icontains=large_query) |
        Q(description__icontains=large_query))
    nb_posts_non_lus = []  # Liste pour l'affichage d'une communaute
    for i in range(len(communautes)):
        if request.user == communautes[i].createur:
            nb_posts_non_lus.append(Post.objects.filter(communaute=communautes[i]).exclude(
                lecteurs__username=request.user.username).count())
        else:
            nb_posts_non_lus.append(Post.objects.filter(communaute=communautes[i], visible=True).exclude(
                lecteurs__username=request.user.username).count())
    communautes = [(communautes[i], nb_posts_non_lus[i]) for i in range(len(communautes))]

    # Recherche dans les createur de communaute
    communautes_par_createur = Communaute.objects.filter(
        Q(createur__username=large_query))
    nb_posts_non_lus_createur = []  # Liste pour l'affichage d'une communaute
    for i in range(len(communautes_par_createur)):
        if request.user == communautes_par_createur[i].createur:
            nb_posts_non_lus_createur.append(Post.objects.filter(communaute=communautes_par_createur[i]).exclude(
                lecteurs__username=request.user.username).count())
        else:
            nb_posts_non_lus_createur.append(Post.objects.filter(communaute=communautes_par_createur[i],
                                                                 visible=True).exclude(
                lecteurs__username=request.user.username).count())
    communautes_par_createur = [(communautes_par_createur[i], nb_posts_non_lus_createur[i]) for i in
                                range(len(communautes_par_createur))]

    accessible_posts = Post.objects.filter(communaute__in=request.user.abonnements.all(),
                                           visible=True)  # On ne regarde que dans les posts des abonnements de l'utilisateur
    # Traitement de la recherche des communaute des posts
    posts = accessible_posts.filter(
        Q(title__icontains=large_query) |
        Q(description__icontains=large_query))
    # Traitement de la recherche des communautes par auteur de post
    posts_par_auteur = accessible_posts.filter(
        Q(auteur__username=large_query))

    return communautes, posts, communautes_par_createur, posts_par_auteur


# Permet à l'utilisateur de marquer un post comme non lu
@login_required()
def marquer_non_lu(request, post_id, url_name):
    post = Post.objects.get(id=post_id)

    # Mise à jour de la liste des utilisateurs qui ont lu le post
    if request.user in post.lecteurs.all():
        post.lecteurs.remove(request.user)

    # Redirige vers la page qui a fait appel à cette view
    if url_name == 'communaute':
        path = reverse(url_name, args=[post.communaute.id])
    else:
        path = reverse(url_name)
    return redirect(path)
