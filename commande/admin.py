import urllib.parse
from django.contrib import admin
from django.utils.html import format_html
from .models import Commande, LigneCommande

class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 1

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'client_nom', 
        'client_telephone', 
        'afficher_produits', 
        'mode_consommation', 
        'date_commande', 
        'statut', 
        'afficher_total', 
        'envoyer_whatsapp'
    )
    
    list_editable = ('statut',)
    list_filter = ('statut', 'mode_consommation', 'date_commande')
    search_fields = ('client_nom', 'client_telephone')
    inlines = [LigneCommandeInline]

    @admin.display(description='Produits commandés')
    def afficher_produits(self, obj):
        items = obj.ligne_commande_set.all()
        details = [f"{item.quantite}x {item.produit.nom}" for item in items]
        return ", ".join(details)

    @admin.display(description='Total')
    def afficher_total(self, obj):
        return f"{obj.total()} FCFA"

    @admin.display(description='WhatsApp')
    def envoyer_whatsapp(self, obj):
        # 1. Nettoyage du numéro (gère le 0 initial, le 226 et les numéros à 8 chiffres)
        raw_phone = str(getattr(obj, 'client_telephone', '')).strip()
        telephone_client = "".join(filter(str.isdigit, raw_phone))

        if telephone_client.startswith('226'):
            num = telephone_client
        elif telephone_client.startswith('0') and len(telephone_client) > 1:
            num = f"226{telephone_client[1:]}"
        elif len(telephone_client) == 8:
            num = f"226{telephone_client}"
        else:
            num = f"226{telephone_client}"

        # 2. Récupération de la liste des produits commandés pour le message
        items = obj.ligne_commande_set.all()
        liste_articles = ", ".join([f"{item.quantite} {item.produit.nom}" for item in items])

        # 3. Message personnalisé avec le détail des produits et le montant total
        if obj.statut == 'livraison':
            msg = f"Bonjour {obj.client_nom} ! Votre commande Belchicken #{obj.id} ({liste_articles}) d'un montant de {obj.total()} FCFA est en cours de livraison."
        elif obj.statut == 'terminée':
            msg = f"Bonjour {obj.client_nom} ! Votre commande Belchicken #{obj.id} ({liste_articles}) est prête !"
        else:
            msg = f"Bonjour {obj.client_nom} ! Nous avons bien reçu votre commande Belchicken #{obj.id} contenant : {liste_articles}. Total : {obj.total()} FCFA."

        msg_encode = urllib.parse.quote(msg)
        url = f"https://wa.me/{num}?text={msg_encode}"

        return format_html(
            '<a href="{}" target="_blank" style="color: #25D366; font-weight: bold; text-decoration: none;">Envoyer</a>',
            url
        )