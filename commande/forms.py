from django import forms
from .models import Commande

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['client_nom', 'client_telephone', 'mode_consommation', 'adresse_livraison']
        widgets = {
            'client_nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom complet'
            }),
            'client_telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre numéro de téléphone'
            }),
            'mode_consommation': forms.Select(attrs={
                'class': 'form-select',
                'id': 'mode_consommation',
                'onchange': 'toggleAdresse(this.value)'
            }),
            'adresse_livraison': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Adresse complète (si livraison)'
            }),
        }