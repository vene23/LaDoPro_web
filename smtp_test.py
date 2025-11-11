import smtplib
from email.mime.text import MIMEText

# Datos de acceso
usuario = "ladopro.unlp@gmail.com"
contraseña = "xawhmiyrkphxjirp"

# Crear el mensaje
msg = MIMEText("Este es un correo de prueba enviado con smtplib.")
msg['Subject'] = "Prueba SMTP directa"
msg['From'] = usuario
msg['To'] = "ladopro.unlp@gmail.com"

# Enviar
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(usuario, contraseña)
    server.sendmail(usuario, ["ladopro.unlp@gmail.com"], msg.as_string())
    server.quit()
    print("Correo enviado correctamente.")
except Exception as e:
    print("Error al enviar:", e)
