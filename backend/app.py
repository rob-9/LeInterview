from flask import Flask, request, jsonify
import threading
import queue
import speech_recognition as sr
import google.generativeai as genai
import pyttsx3

app = Flask(__name__)

# Global Variables
transcription_queue = queue.Queue()
response_queue = queue.Queue()
stop_threads = False

# API Configuration
GEMINI_API_KEY = "AIzaSyDCp0XLchwdXv1rG3U4wXY85h6CFh_1wBA"
genai.configure(api_key=GEMINI_API_KEY)

# Function to get Gemini response using the Gemini SDK
def get_gemini_response(prompt):
    try:
        interview_context = """
        You are helping a friend with a mock interview. The following text is part of a mock interview. 
        Your task is to provide really short friendly feedback on how your friend can prove their speaking
        """
        full_prompt = interview_context + "\n" + prompt

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(full_prompt, stream=True)
        generated_content = ""
        for chunk in response:
            generated_content += chunk.text

        return generated_content

    except Exception as e:
        return f"Error communicating with Gemini API: {e}"

# Function to handle voice input (speech recognition)
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5)
            transcription = recognizer.recognize_google(audio)
            return jsonify({"transcription": transcription})

    except sr.WaitTimeoutError:
        return jsonify({"error": "No speech detected. Retrying..."}), 400
    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand audio."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to get feedback from Gemini
@app.route('/feedback', methods=['POST'])
def get_feedback():
    prompt = request.json.get("text", "")
    feedback = get_gemini_response(prompt)
    return jsonify({"feedback": feedback})

# Function to handle text-to-speech generation
@app.route('/speak', methods=['POST'])
def speak():
    text = request.json.get("text")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    return jsonify({"message": "Speech generated"}), 200

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
