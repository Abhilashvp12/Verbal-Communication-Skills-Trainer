from flask import Blueprint, render_template, request, jsonify
import speech_recognition as sr
from gtts import gTTS
import os
import wave
from config import query_mistral
from flask_cors import CORS

voice_bp = Blueprint('voice', __name__)
CORS(voice_bp)

UPLOAD_FOLDER = "uploads"
AUDIO_RESPONSE_FOLDER = "static/audio"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_RESPONSE_FOLDER, exist_ok=True)

@voice_bp.route('/voice')
def voice_page():
    return render_template('voice.html')

@voice_bp.route('/voice_process', methods=['POST'])
def voice_process():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file uploaded'}), 400

    audio_file = request.files['audio']
    wav_path = os.path.join(UPLOAD_FOLDER, "temp_audio.wav")
    response_audio_path = os.path.join(AUDIO_RESPONSE_FOLDER, "response_audio.mp3")

    try:
        # Save the uploaded file
        audio_file.save(wav_path)

        # Verify it's a valid WAV file (PCM-encoded)
        with wave.open(wav_path, "rb") as wav_file:
            if wav_file.getnchannels() not in [1, 2]:
                return jsonify({'error': 'Invalid WAV format: must be mono or stereo PCM'}), 400
            if wav_file.getsampwidth() not in [1, 2]:
                return jsonify({'error': 'Invalid WAV format: must be 8-bit or 16-bit PCM'}), 400
            if wav_file.getframerate() < 8000 or wav_file.getframerate() > 48000:
                return jsonify({'error': 'Invalid sample rate: must be between 8kHz and 48kHz'}), 400

        # Recognize speech
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)
            try:
                # Recognize speech with explicit language
                text = recognizer.recognize_google(audio_data, language="en-US")
            except sr.UnknownValueError:
                return jsonify({'error': 'Could not understand the audio'}), 400
            except sr.RequestError:
                return jsonify({'error': 'Speech recognition service unavailable'}), 500

        # Get AI response using Mistral model
        ai_response = query_mistral(text)

        # Convert AI response to speech
        tts = gTTS(text=ai_response, lang='en')
        tts.save(response_audio_path)

        return jsonify({
            'text': text,
            'response': ai_response,
            'audio_url': f"/static/audio/response_audio.mp3"
        })

    except Exception as e:
        return jsonify({'error': f"Processing error: {str(e)}"}), 500

    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)
