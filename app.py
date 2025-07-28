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
            model="gpt-4.1-mini",  # or gpt-3.5-turbo / gpt-4.1-mini
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

def generate_inventory_insight(products, sales_orders, purchase_orders):
    try:
        prompt = (
            "You're an expert inventory analyst. Based on the following data, generate a detailed summary, "
            "top-selling products, slow-moving items, and reorder suggestions:\n\n"
            f"Products:\n{products}\n\n"
            f"Sales Orders:\n{sales_orders}\n\n"
            f"Purchase Orders:\n{purchase_orders}\n"
        )

        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are an AI inventory assistant that provides insights and suggestions."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ Error generating insight: {str(e)}"


# Note: No app.run() — Render or Gunicorn handles that
