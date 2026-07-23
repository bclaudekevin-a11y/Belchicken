from django.urls import path
from . import views

app_name = 'commande'

urlpatterns = [
    # URL pour afficher la page du panier et passer la commande
    path('creer/', views.creer_commande, name='commande'),
    
    # URL de confirmation une fois la commande validée avec succès
    path('confirmation/<int:commande_id>/', views.confirmation_commande, name='confirmation_commande'),
     path('panier/', views.voir_panier, name='voir_panier'),
    path('panier/modifier/<int:produit_id>/<str:action>/', views.modifier_quantite, name='modifier_quantite'),
]