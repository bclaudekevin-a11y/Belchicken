from django.db import models
from menu.models import Produit



class Commande(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('livraison', 'En cours de livraison'),
        ('terminée', 'terminée'),
    ]

    MODE_CHOICES = [
        ('sur_place', 'Sur place'),
        ('a_emporter', 'À emporter'),
        ('livraison', 'Livraison'),
    ]

    client_nom = models.CharField(max_length=200)
    client_telephone = models.CharField(max_length=20)
    mode_consommation = models.CharField(max_length=20, choices=MODE_CHOICES, default='sur_place')
    adresse_livraison = models.CharField(max_length=255, blank=True, null=True)
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=20, 
        choices=STATUT_CHOICES, 
        default='en_attente'
    )

    def _str_(self):
        return f"Commande #{self.id} - {self.client_nom}"

    def total(self):
        # Calcule le total basé sur le prix unitaire historisé
        return sum(ligne.sous_total() for ligne in self.lignes.all())


class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    
    # Champ crucial : garde le prix exact au moment de l'achat
    prix_unitaire = models.DecimalField(
        max_length=10, 
        decimal_places=2, 
        max_digits=10, 
        null=True, 
        blank=True
    )

    def save(self, *args, **kwargs):
        # Fixe automatiquement le prix si non renseigné
        if not self.prix_unitaire and self.produit:
            if getattr(self.produit, 'prix_promo', None):
                self.prix_unitaire = self.produit.prix_promo
            else:
                self.prix_unitaire = self.produit.prix
        super().save(*args, **kwargs)

    def _str_(self):
        return f"{self.quantite} x {self.produit.nom}"

    def sous_total(self):
        return (self.prix_unitaire or 0) * self.quantite