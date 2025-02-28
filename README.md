# Verbal-Communication-Skills-Trainer

The Verbal Communication Skills Trainer is an AI-powered web application designed to help users improve their verbal communication through:

Chat Training – Engage in conversations with AI for practice.
Voice Training – Speak into the system and receive real-time feedback.
Assessment Module – Submit text or audio presentations for AI evaluation.
This project integrates a locally downloaded Mistral model and provides an option to switch to OpenAI’s API for AI responses.

Features
✅ Chat-based conversation training
✅ Voice input with AI feedback
✅ Structured assessment with scoring
✅ Support for multiple AI models (Mistral & OpenAI)
✅ Modular code structure for easy scalability

📂 Verbal-Communication-Trainer  
 ├── 📂 templates/          # HTML files for frontend UI  
 │   ├── assess.html  
 │   ├── chat.html  
 │   ├── index.html  
 │   ├── train.html  
 │   ├── voice.html             
 ├── .env                   # Environment variables (OpenAI API key, etc.)  
 ├── app.py                 # Main application file  
 ├── assess.py              # Handles assessment module  
 ├── chat.py                # Chat-based training module  
 ├── config.py              # AI model configurations (Mistral & OpenAI)  
 ├── train.py               # Training module  
 ├── voice.py               # Voice processing module  
 ├── training_data.json      # Predefined training questions  
 ├── assessment_data.json    # Assessment evaluation criteria 
 ├── requirements.txt

