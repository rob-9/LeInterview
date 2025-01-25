// Function to change the code language
function changeLanguage(language) {
    let code = '';

    if (language === 'java') {
        code = `public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}`;
    } else if (language === 'cpp') {
        code = `#include <iostream>
using namespace std;

int main() {
  cout << "Hello, World!" << endl;
  return 0;
}`;
    } else if (language === 'python') {
        code = `print("Hello, World!")`;
    }

    document.getElementById('codeBlock').value = code;
}

// Set default language to Java when the page loads
window.onload = function() {
    changeLanguage('java');
};

// Function to start voice recognition
function startVoiceRecognition() {
    fetch('http://127.0.0.1:5000/transcribe', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data.transcription) {
            document.getElementById('transcriptionResult').innerText = `You said: ${data.transcription}`;
        } else {
            document.getElementById('transcriptionResult').innerText = `Error: ${data.error}`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to get Gemini feedback based on the transcription
function getGeminiFeedback() {
    const transcription = document.getElementById('transcriptionResult').innerText.replace("You said: ", "");
    
    fetch('http://127.0.0.1:5000/feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            text: transcription,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.feedback) {
            document.getElementById('geminiFeedbackResult').innerText = `Gemini Feedback: ${data.feedback}`;
        } else {
            document.getElementById('geminiFeedbackResult').innerText = 'Error: Could not fetch feedback';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
