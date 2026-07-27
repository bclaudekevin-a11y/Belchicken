from django.urls import path
from . import views
app_name='menu'

urlpatterns=[
    path('',views.accueil,name='accueil'),
    path('categorie/<int:categorie_id>/',views.categorie_detail, name="categorie_detail"),
    path('ajouter-au-panier/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('recherche/',views.recherche_produit, name='recherche'),
    path('produit/<int:produit_id>/',views.detail_produit, name='detail_produit'),
]
