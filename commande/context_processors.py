# commande/context_processors.py

def panier_counter(request):
    total_articles = 0
    panier = request.session.get('panier', {})
    if panier:
        total_articles = sum(panier.values())
    return {'quantite_totale_panier': total_articles}