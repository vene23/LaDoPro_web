# init_superuser.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventario_lab.settings")
django.setup()

from django.contrib.auth.models import User

USERNAME = "ladopro"        # <-- Poné el usuario que quieras
EMAIL = "vene_23@hotmail.com"
PASSWORD = "2025ladopro3"   # <-- PONE TU CLAVE REAL

if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD
    )
    print(">>> Superusuario creado correctamente")
else:
    print(">>> El superusuario ya existe, no se creó uno nuevo.")
