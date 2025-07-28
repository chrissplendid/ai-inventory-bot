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
    """Health check endpoint."""
    return "✅ AI Inventory Assistant is running."

@app.route('/chat', methods=['POST'])
def chat():
    """
    Generic chat with AI. No inventory data is considered.
    Payload: { user_message: "..." }
    """
    data = request.get_json()
    user_message = data.get('user_message', '').strip()

    if not user_message:
        return jsonify({'reply': '❌ No message received.'}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "You are a helpful inventory assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'reply': f'⚠️ Error: {str(e)}'}), 500

@app.route('/analyze-inventory', methods=['POST'])
def analyze_inventory():
    """
    Returns high-level AI-generated insights from full inventory data.
    Payload: { products, sales_orders, purchase_orders, token }
    """
    data = request.get_json()
    products = data.get('products', [])
    sales_orders = data.get('sales_orders', [])
    purchase_orders = data.get('purchase_orders', [])
    token = data.get('token', '')

    # Optionally validate token here...

    try:
        insight = generate_inventory_insight(products, sales_orders, purchase_orders)
        return jsonify({'insight': insight})
    except Exception as e:
        return jsonify({'insight': f'⚠️ Error analyzing data: {str(e)}'}), 500

@app.route('/ask-inventory', methods=['POST'])
def ask_inventory():
    """
    User sends a natural-language question with inventory data.
    AI responds based strictly on that data.
    Payload: { user_message, products, sales_orders, purchase_orders }
    """
    data = request.get_json()
    user_message = data.get('user_message', '').strip()
    products = data.get('products', [])
    sales_orders = data.get('sales_orders', [])
    purchase_orders = data.get('purchase_orders', [])

    if not user_message:
        return jsonify({'reply': '❌ Please include your question.'}), 400

    try:
        prompt = (
            "You are an inventory assistant. Answer the user's question based ONLY on the provided data.\n\n"
            f"User's Question: {user_message}\n\n"
            f"Products:\n{products}\n\n"
            f"Sales Orders:\n{sales_orders}\n\n"
            f"Purchase Orders:\n{purchase_orders}\n\n"
            "Do not guess. If the answer cannot be found, say 'I do not have enough information.'"
        )

        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "You are an intelligent assistant trained on inventory data."},
                {"role": "user", "content": prompt}
            ]
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f'⚠️ Error processing request: {str(e)}'}), 500


def generate_inventory_insight(products, sales_orders, purchase_orders):
    """
    Generates an overall summary from raw data using OpenAI.
    """
    prompt = (
        "You are an AI inventory analyst. Analyze the following inventory dataset and provide:\n"
        "- Total products\n"
        "- Sales and purchasing trends\n"
        - "Top-selling items (based on quantity_sold)\n"
        "- Low-stock or stock-alert items\n"
        "- Suggestions on what to restock\n"
        "- Any anomalies or insights\n\n"
        f"Products:\n{products}\n\n"
        f"Sales Orders:\n{sales_orders}\n\n"
        f"Purchase Orders:\n{purchase_orders}"
    )

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides inventory summaries and insights."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# No app.run() — managed by Render or Gunicorn
