from flask import Flask, request, render_template, redirect, url_for
from googletrans import Translator
from gtts import gTTS
import os
import speech_recognition as sr

app = Flask(__name__)

# Initialize the translator
translator = Translator()

# Sample user data for personalized learning paths
user_data = {
    'user1': {'progress': 50, 'performance': 'average'},  # Example user data
}

def translate_to_finnish(text, src_lang='my', dest_lang='fi'):
    """Translate text from Myanmar to Finnish."""
    translation = translator.translate(text, src=src_lang, dest=dest_lang)
    return translation.text

def text_to_speech(text, lang='fi'):
    """Convert text to speech and play it."""
    tts = gTTS(text=text, lang=lang, slow=False)
    filename = 'temp.mp3'
    tts.save(filename)
    os.system(f'start {filename}')  # For Windows
    # os.system(f'afplay {filename}')  # For macOS

def recognize_speech_from_mic():
    """Recognize speech from the microphone and return it as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language='my')
            return text
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Sorry, there was an error with the speech recognition service."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form['text']
    translated_text = translate_to_finnish(text)
    return render_template('index.html', translated_text=translated_text)

@app.route('/speak', methods=['POST'])
def speak():
    text = request.form['text']
    text_to_speech(text)
    return render_template('index.html', message="Playing pronunciation")

@app.route('/speech', methods=['POST'])
def speech():
    spoken_text = recognize_speech_from_mic()
    translated_text = translate_to_finnish(spoken_text)
    return render_template('index.html', translated_text=translated_text, spoken_text=spoken_text)

@app.route('/personalized')
def personalized():
    # Example of personalized learning path based on user data
    user_id = 'user1'  # Example user ID
    user = user_data.get(user_id, {})
    progress = user.get('progress', 0)
    performance = user.get('performance', 'unknown')
    # Adjust learning content based on user progress and performance
    return render_template('personalized.html', progress=progress, performance=performance)

@app.route('/community')
def community():
    # Simple community features (mock-up)
    return render_template('community.html')

if __name__ == "__main__":
    app.run(debug=True)
