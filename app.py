import os
import base64
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get VirusTotal API key from environment variables
VT_API_KEY = os.getenv("VT_API_KEY")

@app.route('/')
def index():
    """
    Serves the main HTML page.
    """
    return render_template('index.html')


@app.route('/api/scan', methods=['POST'])
def scan_url():
    """
    Receives a URL, scans it using VirusTotal, and returns the security status.
    """
    # Check for API key
    if not VT_API_KEY:
        return jsonify({"error": "VirusTotal API key is not configured."}), 500

    # Get URL from request body
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "URL is required in the request body."}), 400

    url_to_scan = data['url']

    # Encode the URL in URL-safe Base64 without padding as required by VirusTotal API v3
    url_id = base64.urlsafe_b64encode(url_to_scan.encode()).decode().strip("=")

    # Prepare the request for VirusTotal API
    vt_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
    headers = {
        "x-apikey": VT_API_KEY,
        "Accept": "application/json"
    }

    try:
        # Query VirusTotal API
        response = requests.get(vt_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        # Process the response
        analysis = response.json()
        stats = analysis.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})

        malicious_count = stats.get("malicious", 0)

        # Determine the security status based on the number of malicious detections
        if malicious_count > 5:
            status = "DANGER"
        elif malicious_count > 0:
            status = "WARNING"
        else:
            status = "SAFE"

        return jsonify({
            "status": status,
            "malicious_count": malicious_count
        })

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            # If the URL is not found, we report it as not found in the VT database.
            return jsonify({"error": "URL not found in VirusTotal database."}), 404
        return jsonify({"error": f"HTTP error occurred: {e}"}), e.response.status_code

    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        return jsonify({"error": f"Error connecting to VirusTotal: {e}"}), 500
    except Exception as e:
        # Handle other unexpected errors
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
