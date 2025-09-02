from flask import Flask, jsonify
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

# Database connection details
DB_HOST = os.getenv('DB_HOST', 'postgres')
DB_NAME = os.getenv('DB_NAME', 'devops_db')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'password123')

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

@app.route("/api/data")
def get_data():
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users;")
            count = cursor.fetchone()[0]
            conn.close()
            
            data = {
                "message": "Hello from Backend!",
                "timestamp": datetime.now().isoformat(),
                "user_count": count,
                "status": "success"
            }
        else:
            data = {
                "message": "Backend running but DB disconnected",
                "timestamp": datetime.now().isoformat(),
                "status": "warning"
            }
    except Exception as e:
        data = {
            "message": "Backend error",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "status": "error"
        }
    
    return jsonify(data)

@app.route("/health")
def health_check():
    return jsonify({"status": "healthy", "service": "backend"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
