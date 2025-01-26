from flask import Flask, render_template, jsonify
import test  # Import the test.py script
import random_code
import gemini_question

app = Flask(__name__)

# Start threads when the app starts
video_thread, audio_thread, gemini_thread, display_thread = test.start_threads()
audio_thread2, gemini_thread2, display_thread2 = gemini_question.start_threads()

@app.route('/')
def index():
    return render_template('interview.html')

@app.route('/get-feedback', methods=['GET'])
def get_feedback():
    # Get the latest feedback from test.py
    feedback = test.get_latest_feedback()
    return jsonify({"feedback": feedback})

@app.route('/random-quest', methods=['GET'])
def random_quest():
    return_question = random_code.find_problem("google")
    return jsonify({"return_question": return_question})

@app.route('/get-question', methods=['GET'])
def get_question():
    question = gemini_question.get_latest_response()
    return jsonify({"question": question})

if __name__ == '__main__':
    app.run(debug=True)
