from flask import Blueprint, render_template, request, jsonify
from config import query_mistral  # Importing from config.py

# Initialize Blueprint
chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat')
def chat_page():
    return render_template('chat.html')

@chat_bp.route('/chat_process', methods=['POST'])
def chat_process():
    """Handles user input, sends it to Mistral model, and returns AI response."""
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({'response': "⚠️ Error: Invalid request format"}), 400

        user_input = data["message"]
        ai_response = query_mistral(user_input)  # Calling function from config.py

        return jsonify({'response': ai_response})
    except Exception as e:
        return jsonify({'response': f"⚠️ Error: {str(e)}"}), 500
