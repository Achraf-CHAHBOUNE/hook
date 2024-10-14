from flask import Flask, request, jsonify
from supabase import create_client
import os
from datetime import datetime
import pytz

# Initialize Flask app
app = Flask(__name__)

# Supabase client initialization
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the Sellix webhook server!"})

@app.route('/webhook', methods=['POST'])
def webhook():
    print("Webhook triggered!")  # Debugging output
    try:
        data = request.json  # Get JSON data from request
        print("Incoming POST Data:", data)  # Logging for debugging

        # Check if data is present
        if not data or 'data' not in data:
            return jsonify({"status": "error", "message": "Invalid payload"}), 400

        # Extract fields based on your payload structure
        order_id = data.get('data', {}).get('id', 'N/A')
        product_id = data.get('data', {}).get('product_id', 'N/A')
        email = data.get('data', {}).get('customer_email', 'N/A')
        product_name = data.get('data', {}).get('product_title', 'N/A')
        total = data.get('data', {}).get('product', {}).get('price_display', 'N/A')
        currency = data.get('data', {}).get('currency', 'N/A')
        status = data.get('data', {}).get('status', 'N/A')

        # Extract custom fields
        custom_fields = data.get('data', {}).get('custom_fields', {})
        full_name = custom_fields.get('full_name', 'N/A')
        country = custom_fields.get('country', 'N/A')
        whatsapp = custom_fields.get('whatsapp', 'N/A')

        # Append all information to Supabase
        created_at = datetime.now(pytz.timezone('Europe/Paris')).isoformat()  # UTC +1 timezone
        response = supabase.table('orders').insert({
            'order_id': order_id,
            'product_id': product_id,
            'full_name': full_name,
            'country': country,
            'whatsapp': whatsapp,
            'email': email,
            'product_name': product_name,
            'total': total,
            'currency': currency,
            'status': status,
            'created_at': created_at
        }).execute()

        return jsonify({"status": "success", "data": response}), 200

    except Exception as e:
        print("Error:", str(e))  # Log error for debugging
        return jsonify({"status": "error", "message": str(e)}), 500

# Use the Flask app as the entry point for Vercel
if __name__ == '__main__':
    app.run()
