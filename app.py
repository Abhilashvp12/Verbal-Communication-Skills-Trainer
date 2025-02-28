from flask import Flask, render_template
from chat import chat_bp
from voice import voice_bp
from train import train_bp
from assess import assess_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(chat_bp)
app.register_blueprint(voice_bp)
app.register_blueprint(train_bp)
app.register_blueprint(assess_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
