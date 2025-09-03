
from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

# Backend API URL (configured for Docker Compose)
BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend:5000/api/data')

@app.route("/")
def index():
    try:
        response = requests.get(BACKEND_URL, timeout=5)
        data = response.json()
    except requests.exceptions.RequestException as e:
        data = {
            "error": f"Cannot connect to backend: {str(e)}",
            "status": "connection_failed"
        }
    except Exception as e:
        data = {
            "error": f"Unexpected error: {str(e)}",
            "status": "error"
        }
    
    return render_template("index.html", data=data)

@app.route("/health")
def health_check():
    return {"status": "healthy", "service": "frontend"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)