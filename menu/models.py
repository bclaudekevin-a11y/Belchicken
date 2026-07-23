from django.db import models

class Categorie(models.Model):
    nom=models.CharField(max_length=200)
    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom=models.CharField(max_length=200)
    prix=models.PositiveIntegerField(default=0)
    image=models.ImageField(upload_to='produits',blank=True,null=True)
    categorie=models.ForeignKey(Categorie,on_delete=models.CASCADE, related_name='produits')
    est_vedette = models.BooleanField(default=False, verbose_name="Produit vedette")
    prix_promo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Prix promotionnel")
    def __str__(self):
        return self.nom

    def pourcentage_reduction(self):
        if self.prix_promo and self.prix > 0:
            reduction = ((self.prix - self.prix_promo) / self.prix) * 100
            return round(reduction)
        return None


