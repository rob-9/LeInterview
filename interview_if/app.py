from flask import Flask, render_template, jsonify
import test  # Import the test.py script

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('interview.html')

@app.route('/run-script', methods=['GET'])
def run_script():
    # Get feedback from test.py
    feedback = test.main()
    return jsonify({"feedback": feedback})

if __name__ == '__main__':
    app.run(debug=True)

