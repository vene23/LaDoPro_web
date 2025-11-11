from django.shortcuts import render, redirect
from .forms import ContactoForm
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage  # para embebido
import os
from django.conf import settings
from django.template.loader import render_to_string
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def inicio(request):
    return render(request, 'public/index.html')
def quienes_somos(request):
    return render(request, 'public/quienes_somos.html')

def servicios(request):
    return render(request, 'public/servicios.html')

def contacto_view(request):
    mensaje_servidor =""
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            asunto = cd.get('asunto') or 'Consulta desde web'
            cuerpo = f"Nombre: {cd['nombre']}\nEmail: {cd['email']}\n\nMensaje:\n{cd['mensaje']}"

            try:
                # 1. Mail principal a Ladopro (gmail) + copia a institucional
                email_obj = EmailMessage(
                    asunto,
                    cuerpo,
                    settings.EMAIL_HOST_USER,
                    ['ladopro.unlp@gmail.com', 'ladopro@fisica.unlp.edu.ar']  # ambos reciben copia
                )
                email_obj.send()

                # 2. Mail de confirmación al usuario con HTML + logo
                html_content = render_to_string("emails/confirmacion_contacto.html", {
                    'nombre': cd['nombre']
                })
                confirmacion = EmailMessage(
                    "Gracias por tu consulta - LaDoPro",
                    html_content,
                    settings.EMAIL_HOST_USER,
                    [cd['email']]
                )
                confirmacion.content_subtype = "html"  # lo marca como HTML
                # Ruta al logo dentro de tu carpeta static
                logo_path = os.path.join(settings.BASE_DIR, "sitio_publico/static/image/lablogo.png")

                if os.path.exists(logo_path):
                    with open(logo_path, "rb") as f:
                        logo_data = f.read()
                        image = MIMEImage(logo_data)
                        image.add_header("Content-ID", "<ladopro_logo>")  # referencia en el HTML
                        confirmacion.attach(image)
                
                confirmacion.send()

                mensaje_servidor = "¡Consulta enviada correctamente! Gracias."
                form = ContactoForm()
            except Exception as e:
                print("Error SMTP:", e)
                mensaje_servidor = "Error al enviar. Intenta luego."
    else:
        form = ContactoForm()
    return render(request, 'public/contacto.html', {'form': form, 'mensaje_servidor': mensaje_servidor})

def notas_interes(request):
    return render(request, 'public/notas_interes.html')

def actividades_academicas(request):
    return render(request, 'public/actividades_academicas.html')

@csrf_exempt
def suscribir_newsletter(request):
    if request.method == "POST":
        try:
            import json
            data = json.loads(request.body)
            email = data.get("email")

            # enviamos al script de Google
            resp = requests.post(
                "https://script.google.com/macros/s/AKfycbxnBZ9ULxa2Y5q34un_RmK3Tsrh7be_lCJHTmq4kHfP0PObcEo6weqz22rLV7h6r_yT/exec",
                json={"email": email},
                timeout=10
            )

            if resp.status_code == 200:
                return JsonResponse({"status": "ok"})
            else:
                return JsonResponse({"status": "error", "message": "Falla en Google Script"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Método no permitido"})
