from flask import Blueprint, render_template, request, jsonify
from config import query_mistral
import random
import json
import os

train_bp = Blueprint('train', __name__)

# File to store training responses
DATA_FILE = "training_data.json"

# Load existing data or initialize an empty list
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        training_data = json.load(f)
else:
    training_data = []

# Training topics categorized by module
TRAINING_TOPICS = {
    "Impromptu Speaking": [
        "Explain why teamwork is important.",
        "What are the benefits of daily exercise?",
        "Describe a time you overcame a challenge.",
    ],
    "Storytelling": [
        "Tell a story about an unforgettable journey.",
        "Narrate a moment when you helped someone.",
        "Describe a fictional adventure of a lost explorer.",
    ],
    "Conflict Resolution": [
        "Handle this situation: 'I'm upset because you missed a deadline.'",
        "Resolve a disagreement between two coworkers.",
        "Respond to a friend who feels ignored by you.",
    ],
}

@train_bp.route('/train')
def train_page():
    return render_template('train.html')

@train_bp.route('/train_topic', methods=['POST'])
def train_topic():
    module = request.json.get("module", "Impromptu Speaking")  # Default to Impromptu Speaking
    if module not in TRAINING_TOPICS:
        return jsonify({'error': 'Invalid module selected'}), 400

    topic = random.choice(TRAINING_TOPICS[module])
    return jsonify({'topic': topic})

@train_bp.route('/train_process', methods=['POST'])
def train_process():
    user_response = request.form['response']
    module = request.form['module']

    if not user_response or not module:
        return jsonify({'error': 'Missing response or module'}), 400

    # Construct prompt for LLM feedback
    feedback_prompt = f"""
    Evaluate this response in the context of {module} training:
    1. **Impromptu Speaking**: Structure, clarity, engagement.
    2. **Storytelling**: Narrative flow, vocabulary, emotional impact.
    3. **Conflict Resolution**: Empathy, assertiveness, effectiveness.
    Provide detailed scores and improvement tips.
    Response: {user_response}
    """
    
    feedback = query_mistral(feedback_prompt)

    # Store user response and feedback
    entry = {"module": module, "response": user_response, "feedback": feedback}
    training_data.append(entry)
    with open(DATA_FILE, "w") as f:
        json.dump(training_data, f, indent=4)

    return jsonify({'feedback': feedback})
