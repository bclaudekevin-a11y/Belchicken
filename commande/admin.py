from django.contrib import admin
from .models import Commande, LigneCommande
from django.utils.html import format_html
import urllib.parse


class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 1
    # Empêche de modifier manuellement le prix unitaire si souhaité
    readonly_fields = ['prix_unitaire']


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'client_nom', 
        'mode_consommation', 
        'date_commande', 
        'statut', 
        'afficher_total',
        'envoyer_whatsapp',
    ]
    readonly_fields = ['envoyer_whatsapp']
    list_filter = ['statut', 'mode_consommation', 'date_commande']
    search_fields = ['client_nom', 'client_telephone']
    inlines = [LigneCommandeInline]

    @admin.display(description='Total')
    def afficher_total(self, obj):
        return f"{obj.total()} FCFA"
    def envoyer_whatsapp(self, obj):
        # On nettoie le numéro pour WhatsApp
        # Ton numéro en texte (avec guillemets)
        mon_numero = "07276613"
        num = f"226{mon_numero[0:]}" if mon_numero.startswith("0") else f"226{mon_numero}"
        # Message selon le statut
        if obj.statut == 'livraison':
            msg = f"Bonjour {obj.client_nom} ! Votre commande Belchicken #{obj.id} est en cours de livraison !,notre livreur vous contactera"
        elif obj.statut == 'terminee':
            msg = f"Bonjour {obj.client_nom} ! Votre commande Belchicken #{obj.id} est prête !"
        else:
            msg = f"Bonjour {obj.client_nom} ! Nous avons bien reçu votre commande Belchicken #{obj.id}."

        msg_encode = urllib.parse.quote(msg)
        url = f"https://wa.me/{num}?text={msg_encode}"

        return format_html(
            '<a href="{}" target="_blank" style="color: #417690; font-weight: bold; text-decoration: underline;">Envoyer WhatsApp</a>', 
            url
        )

    envoyer_whatsapp.short_description = "Notification"

    def get_queryset(self, request):
        # Optimise les performances SQL en chargeant les lignes et produits liés en une seule requête
        qs = super().get_queryset(request)
        return qs.prefetch_related('lignes__produit')
    
class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 0

#@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    # Les colonnes affichées dans l'admin (ajoute 'envoyer_whatsapp' à la fin)
    list_display = ('id', 'client_nom', 'client_telephone', 'mode_consommation', 'statut', 'envoyer_whatsapp')
    list_filter = ('statut', 'mode_consommation')
    inlines = [LigneCommandeInline]

    