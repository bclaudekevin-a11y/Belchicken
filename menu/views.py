from django.shortcuts import render,get_object_or_404,redirect
from .models import Categorie, Produit
from django.http import JsonResponse
def accueil(request):
    produits_vedettes=Produit.objects.filter(est_vedette=True)
    return render(request, 'menu/accueil.html', {'produits_vedettes': produits_vedettes})

def categorie_detail(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    produits = categorie.produits.all()
    return render(request, 'menu/categorie_detail.html', {
        'categorie': categorie,
        'produits': produits
    })
def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    panier = request.session.get('panier', {})
    
    # Cast en string car les clés des sessions JSON sont des chaînes
    p_id = str(produit_id)
    if p_id in panier:
        panier[p_id] += 1
    else:
        panier[p_id] = 1

    request.session['panier'] = panier

    # Calcul du nombre total d'articles et du montant total
    total_articles = sum(panier.values())
    
    # Si la requête est en AJAX (depuis JavaScript)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': f"{produit.nom} ajouté au panier !",
            'total_articles': total_articles
        })
    
    # Fallback si JS est désactivé
    return redirect('menu:accueil')
