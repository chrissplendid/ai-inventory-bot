from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "AI Inventory Assistant is running."

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('user_message', '')

    if not user_message:
        return jsonify({'reply': 'No message received.'}), 400

    try:
        completion = client.chat.completions.create(
            model="gpt-4-1106-preview",  # or gpt-3.5-turbo / gpt-4.1-mini
            messages=[
                {"role": "system", "content": "You are a helpful inventory assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = completion.choices[0].message.content
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'reply': f'Error: {str(e)}'}), 500

@app.route('/analyze-inventory', methods=['POST'])
def analyze_inventory():
    data = request.get_json()

    products = data.get('products', [])
    sales_orders = data.get('sales_orders', [])
    purchase_orders = data.get('purchase_orders', [])
    token = data.get('token', '')

    # Optional: Token validation logic here

    # Generate insight summary
    insight = generate_inventory_insight(products, sales_orders, purchase_orders)
    
    return jsonify({'insight': insight})

def generate_inventory_insight(products, sales, purchases):
    # Simple logic, can be replaced with AI-generated summary
    return (
        f"📊 Inventory Summary:\n"
        f"- Total Products: {len(products)}\n"
        f"- Sales Orders: {len(sales)}\n"
        f"- Purchase Orders: {len(purchases)}\n\n"
        f"You can ask me to identify top-selling items or suggest what to restock!"
    )

# Note: No app.run() — Render or Gunicorn handles that
