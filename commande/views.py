from django.shortcuts import render, redirect, get_object_or_404
from .forms import CommandeForm
from .models import Commande, LigneCommande
from menu.models import Produit
from django.http import JsonResponse

def creer_commande(request):
    panier = request.session.get('panier', {})

    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            # 1. Sauvegarde automatique de la commande via le Form
            commande = form.save()

            # 2. Création des lignes de commande
            for produit_id, quantite in panier.items():
                produit = get_object_or_404(Produit, id=produit_id)
                LigneCommande.objects.create(
                    commande=commande,
                    produit=produit,
                    quantite=quantite
                )

            # 3. Vider le panier
            request.session['panier'] = {}

            # 4. Redirection vers la page de confirmation
            return redirect('commande:confirmation_commande', commande_id=commande.id)
    else:
        form = CommandeForm()

    return render(request, 'commande/commande.html', {'form': form, 'panier': panier})


def confirmation_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    return render(request, 'commande/confirmation.html', {'commande': commande})

def ajouter_au_panier(request, produit_id):
    # 1. On récupère le panier courant depuis la session (ou un dictionnaire vide {})
    panier = request.session.get('panier', {})
    
    # 2. On récupère la quantité envoyée par le formulaire (par défaut 1)
    quantite = int(request.POST.get('quantite', 1))
    
    # Convertir l'ID en chaîne de caractères car les clés JSON de session sont des strings
    produit_id_str = str(produit_id)

    # 3. On ajoute ou on incrémente la quantité
    if produit_id_str in panier:
        panier[produit_id_str] += quantite
    else:
        panier[produit_id_str] = quantite

    # 4. On enregistre le panier mis à jour dans la session
    request.session['panier'] = panier

    # 5. On redirige directement le client vers la page de commande
    return redirect('commande:creer_commande')

def voir_panier(request):
    panier = request.session.get('panier', {})
    articles = []
    total_general = 0

    for produit_id, quantite in panier.items():
        try:
            produit = Produit.objects.get(id=produit_id)
            total_article = produit.prix * quantite
            total_general += total_article
            articles.append({
                'produit': produit,
                'quantite': quantite,
                'total_article': total_article,
            })
        except Produit.DoesNotExist:
            continue

    context = {
        'articles': articles,
        'total_general': total_general,
    }
    return render(request, 'commande/panier.html', context)


def modifier_quantite(request, produit_id, action):
    panier = request.session.get('panier', {})
    p_id = str(produit_id)

    if p_id in panier:
        if action == 'plus':
            panier[p_id] += 1
        elif action == 'moins':
            panier[p_id] -= 1
            if panier[p_id] <= 0:
                del panier[p_id]
        elif action == 'supprimer':
            del panier[p_id]

        request.session['panier'] = panier

    return redirect('commande:voir_panier')