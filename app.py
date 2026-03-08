import os
import base64
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()
app = Flask(__name__)

# Get VirusTotal API key
VT_API_KEY = os.getenv("VT_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scan', methods=['POST'])
def scan_url():
    if not VT_API_KEY:
        return jsonify({"error": "Configuración del servidor incompleta (Falta API Key)."}), 500

    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Falta la URL en la petición."}), 400

    url_to_scan = data['url'].strip()

    # 1. MEJORA: Normalización básica de URL
    # Si el usuario no pone protocolo, asumimos https://
    if not url_to_scan.startswith(('http://', 'https://')):
        url_to_scan = 'https://' + url_to_scan

    try:
        # Encode URL for VirusTotal API v3
        url_id = base64.urlsafe_b64encode(url_to_scan.encode()).decode().strip("=")

        vt_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
        headers = {
            "x-apikey": VT_API_KEY,
            "Accept": "application/json"
        }

        response = requests.get(vt_url, headers=headers)

        # 2. MEJORA: Manejo específico de URL no encontrada (404)
        if response.status_code == 404:
            return jsonify({
                "status": "UNKNOWN",
                "message": "URL no analizada previamente por VirusTotal.",
                "malicious_count": 0
            })

        response.raise_for_status()

        # Process response
        analysis = response.json()
        attributes = analysis.get("data", {}).get("attributes", {})
        stats = attributes.get("last_analysis_stats", {})

        malicious_count = stats.get("malicious", 0)
        suspicious_count = stats.get("suspicious", 0)

        # 3. MEJORA: Lógica de seguridad más estricta
        # En ciberseguridad, >0 ya es riesgo.
        total_flags = malicious_count + suspicious_count

        if total_flags >= 3:
            status = "DANGER"
            msg = f"¡Peligro! {malicious_count} motores de seguridad detectaron amenazas."
        elif total_flags > 0:
            status = "WARNING"
            msg = f"Precaución: {malicious_count} motores marcaron este sitio como sospechoso."
        else:
            status = "SAFE"
            msg = "El enlace parece limpio (0 detecciones)."

        return jsonify({
            "status": status,
            "malicious_count": malicious_count,
            "message": msg,
            "scan_date": attributes.get("last_analysis_date", "N/A") # Dato extra útil
        })

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to VirusTotal: {e}")
        return jsonify({"error": "Error de conexión con el servicio de escaneo."}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Ocurrió un error inesperado en el servidor."}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    # En producción, debug debe ser False por seguridad.
    app.run(host='0.0.0.0', port=port, debug=False)
