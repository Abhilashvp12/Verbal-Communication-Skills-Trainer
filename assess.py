from flask import Blueprint, render_template, request, jsonify
from config import query_mistral
import json
import os
import speech_recognition as sr
import librosa
import soundfile as sf

# Initialize Blueprint
assess_bp = Blueprint('assess', __name__)

# File to store assessments
DATA_FILE = "assessment_data.json"

# Load existing data or initialize an empty list
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        assessments = json.load(f)
else:
    assessments = []

# Ensure the uploads directory exists
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Function to transcribe audio using SpeechRecognition
def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()

    try:
        # Load the audio file using librosa
        y, sample_rate = librosa.load(audio_path, sr=None)  # Rename sr to sample_rate

        # Convert to WAV format and save temporarily
        wav_path = audio_path.replace(os.path.splitext(audio_path)[1], ".wav")
        sf.write(wav_path, y, sample_rate)  # Use sample_rate here

        # Transcribe the WAV file
        with sr.AudioFile(wav_path) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not transcribe audio."
    except sr.RequestError:
        return "Error with the transcription service."
    except Exception as e:
        return f"Error processing audio: {str(e)}"

# Route for the assessment page
@assess_bp.route('/assess')
def assess_page():
    return render_template('assess.html')

# Route to process assessment
@assess_bp.route('/assess_process', methods=['POST'])
def assess_process():
    text = None

    # Handle text submission
    if 'script' in request.form and request.form['script'].strip():
        text = request.form['script'].strip()

    # Handle voice file submission
    elif 'voice' in request.files:
        audio_file = request.files['voice']
        if audio_file.filename:
            # Save the uploaded file
            audio_path = os.path.join(UPLOAD_DIR, audio_file.filename)
            audio_file.save(audio_path)

            # Transcribe the audio file
            text = transcribe_audio(audio_path)

    if not text:
        return jsonify({'error': 'No valid text or voice input provided.'}), 400

    # Construct LLM prompt
    feedback_prompt = f"""
    Evaluate this presentation:
    1. **Structure (10 pts)**: Is there a clear intro, body, and conclusion?
    2. **Delivery (10 pts)**: Assess pacing, tone, and clarity.
    3. **Content (10 pts)**: Evaluate persuasiveness, vocabulary, and relevance.
    Provide scores and specific improvement suggestions.
    Text: {text}
    """
    
    feedback = query_mistral(feedback_prompt)

    # Store the response and feedback
    entry = {"response": text, "feedback": feedback}
    assessments.append(entry)
    with open(DATA_FILE, "w") as f:
        json.dump(assessments, f, indent=4)

    return jsonify({'feedback': feedback})