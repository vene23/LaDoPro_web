import os
import django
from django.core.mail import EmailMessage
from django.conf import settings

# Inicializar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario_lab.settings')
django.setup()

# Crear y enviar el correo
email = EmailMessage(
    'Prueba directa',
    'Este es un mensaje de prueba enviado desde consola.',
    settings.EMAIL_HOST_USER,
    ['vene_23@hotmail.com']  # Cambiá por el destinatario que quieras probar
)
email.send()
print("Correo enviado (si no hay error)")
