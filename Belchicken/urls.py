
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User

if not User.objects.filter(username="Claude").exists():
    User.objects.create_superuser("Claude", "bclaudekevin@gmail.com", "Kevin6059")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('menu.urls')),
    path('commande/',include('commande.urls')),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
