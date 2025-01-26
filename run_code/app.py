from flask import Flask, request, jsonify
import subprocess
from flask_cors import CORS  # Add this for handling CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return "Python Code Interpreter API is running!"

@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.json
    code = data.get('code', '')

    try:
        # Execute the Python code
        result = subprocess.run(
            ['python', '-c', code],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return jsonify({ 'output': result.stdout })
        else:
            return jsonify({ 'error': result.stderr })
    except Exception as e:
        return jsonify({ 'error': str(e) })

if __name__ == '__main__':
    app.run(debug=True, port = 8080)