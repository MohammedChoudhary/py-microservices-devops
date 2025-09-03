
import time
import requests
import json
from datetime import datetime
import os

# Configuration
BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend:5000')
LOG_FILE = '/app/logs/service.log'
CHECK_INTERVAL = 10  # seconds

def write_log(message):
    """Write log message to file with timestamp"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}\n"
    
    # Ensure log directory exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry)
    
    print(log_entry.strip())  # Also print to console

def check_backend_health():
    """Check if backend service is healthy"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            write_log(f"✅ Backend health check: {data}")
            return True
        else:
            write_log(f"⚠️ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        write_log(f"❌ Backend health check failed: {str(e)}")
        return False

def monitor_backend_api():
    """Monitor the backend API endpoint"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/data", timeout=5)
        if response.status_code == 200:
            data = response.json()
            write_log(f" API Response: status={data.get('status', 'unknown')}, user_count={data.get('user_count', 'N/A')}")
        else:
            write_log(f"⚠️ API returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        write_log(f"❌ API check failed: {str(e)}")

def main():
    write_log("Logger service started")
    write_log(f"Monitoring backend at: {BACKEND_URL}")
    write_log(f"Logging to: {LOG_FILE}")
    write_log(f"Check interval: {CHECK_INTERVAL} seconds")
    
    while True:
        try:
            # Check backend health
            backend_healthy = check_backend_health()
            
            # If backend is healthy, also check the API
            if backend_healthy:
                monitor_backend_api()
            
            # Wait before next check
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            write_log("🛑 Logger service stopping...")
            break
        except Exception as e:
            write_log(f"🚨 Unexpected error in logger: {str(e)}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()