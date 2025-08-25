import os
import random
import subprocess
import threading
import queue
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import speech_recognition as sr
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Global Variables
transcription_queue = queue.Queue()
response_queue = queue.Queue()
stop_threads = False
feedback_result = None

# API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("Warning: GEMINI_API_KEY environment variable not set")

def get_gemini_response(prompt):
    """Generate feedback response using Gemini AI"""
    try:
        feedback_context = """
        You are helping a friend with a mock interview. The following text is part of a mock interview. 
        Your task is to provide really short friendly feedback on how your friend can improve their speaking.
        Start feedback with a score between 0-9. E.g. "8; <feedback>" 
        Please calibrate your score so that the 'average' person interview will score 5.
        """
        feedback_prompt = feedback_context + "\n" + prompt

        model = genai.GenerativeModel("gemini-1.5-flash")
        feedback_response = model.generate_content(feedback_prompt, stream=True)

        feedback_content = ""
        for chunk in feedback_response:
            feedback_content += chunk.text

        return feedback_content

    except Exception as e:
        return f"Error communicating with Gemini API: {e}"

def audio_transcription():
    """Handle audio transcription in background thread"""
    global stop_threads
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while not stop_threads:
        try:
            with microphone as source:
                print("Listening for speech...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                transcription = recognizer.recognize_google(audio)
                print(f"Transcription: {transcription}")
                transcription_queue.put(transcription)

        except sr.WaitTimeoutError:
            print("Silence detected for 5 seconds.")
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except Exception as e:
            print(f"Error during audio transcription: {e}")

def process_gemini_responses():
    """Process Gemini responses in background thread"""
    global stop_threads, feedback_result
    while not stop_threads:
        try:
            transcription = None
            try:
                transcription = transcription_queue.get(timeout=1)
            except queue.Empty:
                pass

            if transcription:
                print(f"Sending to Gemini: {transcription}")
                feedback_result = get_gemini_response(transcription)
                response_queue.put(feedback_result)
                print(f"Gemini Response: {feedback_result}")

        except Exception as e:
            print(f"Error processing Gemini response: {e}")

def start_threads():
    """Start background threads for audio processing"""
    global stop_threads
    stop_threads = False

    audio_thread = threading.Thread(target=audio_transcription)
    gemini_thread = threading.Thread(target=process_gemini_responses)

    audio_thread.start()
    gemini_thread.start()

    return audio_thread, gemini_thread

def find_problem(company_name):
    """Find a problem for the given company"""
    try:
        with open("templates/companies.txt", 'r') as file:
            problems = []
            for line in file.readlines():
                if line.startswith(company_name):
                    problems.append(line[len(company_name) + 1: -1])
            return random.choice(problems) if problems else "Two Sum"
    except FileNotFoundError:
        return "Two Sum"

def get_response_from_gemini(problem_name):
    """Get problem description from Gemini"""
    if not GEMINI_API_KEY:
        return "Please set GEMINI_API_KEY environment variable"
    
    model = genai.GenerativeModel("gemini-1.5-flash")   
    try:
        response = model.generate_content(
            f"Very briefly display the problem {problem_name} from leetcode and one sample output"
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# API Routes
@app.route('/get-feedback', methods=['GET'])
def get_feedback():
    """Get the latest feedback from AI"""
    global feedback_result
    return jsonify({"feedback": feedback_result})

@app.route('/start-interview', methods=['POST'])
def start_interview():
    """Start the interview process"""
    global stop_threads
    stop_threads = False
    print("Starting interview...")
    start_threads()
    return jsonify({"message": "Interview started"})

@app.route('/stop-interview', methods=['POST'])
def stop_interview():
    """Stop the interview process"""
    global stop_threads
    stop_threads = True
    return jsonify({"message": "Interview stopped"})

@app.route('/execute', methods=['POST'])
def execute_code():
    """Execute code in different programming languages"""
    data = request.json
    code = data.get('code')
    language = data.get('language', 'python').lower()

    if language == 'python':
        try:
            result = subprocess.run(
                ['python3', '-c', code], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            output = result.stdout if result.returncode == 0 else result.stderr
        except subprocess.TimeoutExpired:
            output = "Code execution timed out"
        except Exception as e:
            output = str(e)
            
    elif language == 'java':
        try:
            with open('Main.java', 'w') as f:
                f.write(code)
            compile_result = subprocess.run(
                ['javac', 'Main.java'], 
                capture_output=True, 
                text=True,
                timeout=10
            )
            if compile_result.returncode != 0:
                output = compile_result.stderr
            else:
                run_result = subprocess.run(
                    ['java', 'Main'], 
                    capture_output=True, 
                    text=True,
                    timeout=10
                )
                output = run_result.stdout if run_result.returncode == 0 else run_result.stderr
            
            # Cleanup
            for file in ['Main.java', 'Main.class']:
                if os.path.exists(file):
                    os.remove(file)
        except subprocess.TimeoutExpired:
            output = "Code execution timed out"
        except Exception as e:
            output = str(e)
            
    elif language == 'c++':
        try:
            with open('main.cpp', 'w') as f:
                f.write(code)
            compile_result = subprocess.run(
                ['g++', 'main.cpp', '-o', 'main'], 
                capture_output=True, 
                text=True,
                timeout=10
            )
            if compile_result.returncode != 0:
                output = compile_result.stderr
            else:
                run_result = subprocess.run(
                    ['./main'], 
                    capture_output=True, 
                    text=True,
                    timeout=10
                )
                output = run_result.stdout if run_result.returncode == 0 else run_result.stderr
            
            # Cleanup
            for file in ['main.cpp', 'main']:
                if os.path.exists(file):
                    os.remove(file)
        except subprocess.TimeoutExpired:
            output = "Code execution timed out"
        except Exception as e:
            output = str(e)
    else:
        output = 'Unsupported language'

    return jsonify({'output': output})

@app.route('/random-quest/<company_name>', methods=['GET'])
def random_quest(company_name):
    """Get a random question for the given company"""
    problem = find_problem(company_name)
    return_question = get_response_from_gemini(problem)
    return jsonify({"return_question": return_question})

# Page Routes
@app.route('/')
def home():
    """Render the home page"""
    return render_template('index.html')

@app.route('/interview')
def interview():
    """Render the interview page"""
    return render_template('interview.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)