from django.shortcuts import render, redirect
from .forms import ContactoForm
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage  # para embebido
import os
import resend
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
    mensaje_servidor = ""

    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            asunto = cd.get('asunto') or 'Consulta desde web'
            cuerpo = f"Nombre: {cd['nombre']}\nEmail: {cd['email']}\n\nMensaje:\n{cd['mensaje']}"

            import resend
            resend.api_key = settings.RESEND_API_KEY

            try:
                # 1) Enviar al laboratorio
                resend.Emails.send({
                    "from": "LaDoPro <onboarding@resend.dev>",
                    "to": [
                        "ladopro.unlp@gmail.com",
                        "ladopro@fisica.unlp.edu.ar"
                    ],
                    "subject": asunto,
                    "text": cuerpo
                })

                # 2) Confirmación al usuario
                html_content = render_to_string(
                    "emails/confirmacion_contacto.html",
                    {'nombre': cd['nombre']}
                )

                resend.Emails.send({
                    "from": "LaDoPro <onboarding@resend.dev>",
                    "to": cd["email"],
                    "subject": "Gracias por tu consulta - LaDoPro",
                    "html": html_content
                })

                mensaje_servidor = "¡Consulta enviada correctamente!"
                form = ContactoForm()

            except Exception as e:
                print("Error Resend:", e)
                mensaje_servidor = "Error al enviar. Intenta luego."

    else:
        form = ContactoForm()

    return render(request, 'public/contacto.html', {
        'form': form,
        'mensaje_servidor': mensaje_servidor
    })

        
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
