document.getElementById('run-button').addEventListener('click', async function () {
  const code = document.getElementById('code-editor').value;
  const outputDiv = document.getElementById('output');

  // Update this URL to match your Flask server
  const apiUrl = 'http://127.0.0.1:8080/execute';

  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ code }),
    });

    const data = await response.json();

    if (data.error) {
      outputDiv.textContent = 'Error: ' + data.error;
    } else {
      outputDiv.textContent = data.output;
    }
  } catch (error) {
    outputDiv.textContent = 'Error: ' + error.message;
  }
});