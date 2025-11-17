from django.shortcuts import render, redirect
from .forms import ContactoForm
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
    mensaje_servidor = ""

    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            asunto = cd.get('asunto') or 'Consulta desde web'
            cuerpo_ladopro = f"Nombre: {cd['nombre']}\nEmail: {cd['email']}\n\nMensaje:\n{cd['mensaje']}"

            # --- HTML para usuario ---
            html_usuario = render_to_string(
                "emails/confirmacion_contacto.html",
                {"nombre": cd["nombre"]}
            )

            # 1) Enviar al laboratorio
            datos_ladopro = {
                "sender": {
                    "name": "LaDoPro Web",
                    "email": "ladopro@brevo.com"        # REMITE DESDE BREVO
                },
                "to": [
                    {"email": "ladopro.unlp@gmail.com"},
                    {"email": "ladopro@fisica.unlp.edu.ar"}
                ],                
                "subject": asunto,
                "textContent": cuerpo_ladopro
            }

            # --- 2) enviar confirmación al usuario ---
            datos_usuario = {
                "sender": {
                    "name": "LaDoPro Web",
                    "email": "ladopro@brevo.com"
                },
                "to": [{"email": cd["email"]}],
                "subject": "Gracias por tu consulta - LaDoPro",
                "htmlContent": html_usuario
            }
            
            print("BREVO_API_KEY:", settings.BREVO_API_KEY)

            # --- Enviar vía API ---
            try:
                headers = {
                    "api-key": settings.BREVO_API_KEY,
                    "Content-Type": "application/json"
                }

                # 1) Mail al laboratorio
                requests.post(
                    "https://api.brevo.com/v3/smtp/email",
                    json=datos_ladopro,
                    headers=headers,
                    timeout=10
                )

                # 2) Mail al usuario
                requests.post(
                    "https://api.brevo.com/v3/smtp/email",
                    json=datos_usuario,
                    headers=headers,
                    timeout=10
                )

                mensaje_servidor = "¡Consulta enviada correctamente!"
                form = ContactoForm()

            except Exception as e:
                print("Error Brevo:", e)
                mensaje_servidor = "Error al enviar. Intenta luego."

    else:
        form = ContactoForm()

    return render(
        request,
        "public/contacto.html",
        {"form": form, "mensaje_servidor": mensaje_servidor}
    )
        
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
