from django.db import migrations
from django.contrib.auth import get_user_model

def create_superuser(apps, schema_editor):
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="Claude", 
            email="bclaudekevin@gmail.com", 
            password="Kevin6059"
        )

class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_produit_est_vedette_produit_prix_pr...'), # Garde bien la dépendance vers ta migration précédente qui est affichée dans ton fichier
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
