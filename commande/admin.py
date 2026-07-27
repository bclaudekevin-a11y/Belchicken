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
        items = obj.lignes.all()
        details = [f"{item.quantite}x {item.produit.nom}" for item in items]
        return ", ".join(details)

    @admin.display(description='Total')
    def afficher_total(self, obj):
        return f"{obj.total()} FCFA"

    @admin.display(description='WhatsApp')
    def envoyer_whatsapp(self, obj):
        raw_phone = str(getattr(obj, 'client_telephone', '')).strip()
        telephone_client = "".join(filter(str.isdigit, raw_phone))

        # Si le numéro commence par 226
        if telephone_client.startswith('226'):
            # S'il manque un chiffre (parce que le 0 a sauté, ex: 226 + 7 chiffres = 10 caractères au total)
            if len(telephone_client) == 10: 
                # On réinsère le 0 juste après le 226 -> 226 + 0 + les 7 chiffres
                num = f"2260{telephone_client[3:]}"
            else:
                num = telephone_client
        # Si le numéro a été enregistré sans le 226 et fait 7 chiffres (ex: 7276613)
        elif len(telephone_client) == 7:
            num = f"2260{telephone_client}"
        # Si le numéro commence par 0 et fait 8 chiffres (ex: 07276613)
        elif telephone_client.startswith('0') and len(telephone_client) == 8:
            num = f"226{telephone_client}" # Le 0 est gardé car l'API WhatsApp l'accepte souvent ou on peut le formater
        else:
            num = f"226{telephone_client}"

        # Récupération de la liste des produits pour le message
        items = obj.lignes.all()
        liste_articles = ", ".join([f"{item.quantite} {item.produit.nom}" for item in items])

        if obj.statut == 'livraison':
            msg = f"Bonjour {obj.client_nom} ! Votre commande Belchicken #{obj.id} ({liste_articles}) d'un montant de {obj.total()} FCFA est en cours de livraison."
        elif obj.statut == 'terminée':
            msg = f"Bonjour {obj.client_nom} ! Votre commande Belchicken #{obj.id} ({liste_articles}) est prête !"
        else:
            msg = f"Bonjour {obj.client_nom} ! Nous avons bien reçu votre commande #{obj.id} contenant : {liste_articles}. Total : {obj.total()} FCFA."

        msg_encode = urllib.parse.quote(msg)
        url = f"https://wa.me/{num}?text={msg_encode}"

        return format_html(
            '<a href="{}" target="_blank" style="color: #25D366; font-weight: bold; text-decoration: none;">Envoyer</a>',
            url
        )