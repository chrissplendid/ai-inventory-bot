from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI 
from inventory_functions import handle_inventory_query
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Read the API key from the environment (unused for now)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client (commented out)
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow requests from your Angular frontend

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('user_message', '')

    # Check if your custom inventory function can answer it
    inventory_response = handle_inventory_query(user_message)
    if inventory_response:
        return jsonify({'reply': inventory_response})

    # Otherwise, fallback to mock response
    # (Real OpenAI call commented out)
    completion = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
             {"role": "system", "content": "You are a helpful inventory assistant."},
            {"role": "user", "content": user_message}
        ]
    )
    answer = completion.choices[0].message.content

    # Instead, just return echo for testing
    # answer = f"You said: {user_message}"
    return jsonify({'reply': answer})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
