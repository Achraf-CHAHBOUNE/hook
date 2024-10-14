from flask import Flask, request, jsonify
from supabase import create_client
import os
from datetime import datetime
import pytz

# Initialize Flask app
app = Flask(__name__)

# Supabase client initialization
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://your_supabase_url')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'your_supabase_key')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the Flask API!"})

@app.route('/webhook', methods=['POST'])
def webhook():
    print("Webhook triggered!")
    try:
        data = request.json
        print("Incoming POST Data:", data)

        if not data or 'data' not in data:
            return jsonify({"status": "error", "message": "Invalid payload"}), 400

        # Extract fields (example, adapt to your data structure)
        order_id = data.get('data', {}).get('id', 'N/A')
        # ... extract other fields as needed

        created_at = datetime.now(pytz.timezone('Europe/Paris')).isoformat()
        # Insert into Supabase or handle the data accordingly

        return jsonify({"status": "success", "order_id": order_id}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run()
