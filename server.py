from flask import Flask, request, jsonify
import smtplib
import random
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite que cualquier página web pueda acceder a este servidor

# Función para generar un código de verificación de 6 dígitos
def generar_codigo():
    return str(random.randint(100000, 999999))

# Configuración del servidor de correo usando variables de entorno
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

def enviar_correo(destinatario, codigo):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            mensaje = f"Subject: Código de verificación\n\nTu código es: {codigo}"
            server.sendmail(EMAIL, destinatario, mensaje)
    except Exception as e:
        print("Error enviando el correo:", e)

@app.route('/suscribirse', methods=['POST'])
def suscribirse():
    datos = request.get_json()
    email = datos.get("email")

    if not email:
        return jsonify({"error": "Falta el email"}), 400

    codigo = generar_codigo()
    enviar_correo(email, codigo)

    return jsonify({"mensaje": "Correo enviado", "codigo": codigo})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render asigna un puerto automáticamente
    app.run(debug=True, host="0.0.0.0", port=port)
