from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os

from inventory_functions import handle_inventory_query

# Load environment variables
load_dotenv()

# Read OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
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

    # Custom inventory query
    inventory_response = handle_inventory_query(user_message)
    if inventory_response:
        return jsonify({'reply': inventory_response})

    # Fallback to OpenAI (mock removed)
    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful inventory assistant."},
            {"role": "user", "content": user_message}
        ]
    )
    answer = completion.choices[0].message.content
    return jsonify({'reply': answer})

# Don’t include app.run() — Render uses gunicorn to start your app
