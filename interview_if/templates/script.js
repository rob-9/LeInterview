document.getElementById('run-code').addEventListener('click', () => {
  const code = codeEditor.getValue();
  const outputDiv = document.getElementById('output');
  outputDiv.textContent = 'Running...';

  // Get the selected language
  const selectedLanguage = document.querySelector('.language-selector button.selected').textContent.toLowerCase();

  // Send the code and language to the Flask backend
  fetch('http://127.0.0.1:5002/execute', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ code: code, language: selectedLanguage }),
  })
    .then(response => response.json())
    .then(data => {
      if (data.output) {
        outputDiv.textContent = data.output;
      } else {
        outputDiv.textContent = 'Error: No output received';
      }
    })
    .catch(error => {
      outputDiv.textContent = `Error: ${error.message}`;
    });
});

//___________________LANGUAGE SWITCHER___________________________

function changeLanguage(language) {
    const codeBlock = document.getElementById('codeBlock'); // The <code> block inside the <pre>

    // Remove any existing language classes from the <code> block
    codeBlock.className = ''; // Clear all classes
    codeBlock.classList.add(`language-${language}`); // Add the new language class


    if (language === 'java') {
        codeBlock.textContent = `public class HelloWorld {
        public static void main(String[] args) {
            System.out.println("Hello, World!");
        }
    }`;

    } else if (language === 'cpp') {
        codeBlock.textContent = `#include <iostream>
    using namespace std;
    
    int main() {
        cout << "Hello, World!" << endl;
        return 0;
    }`;
    } else if (language === 'python') {
        codeBlock.textContent = `print("Hello, World!")`;
    } else if (language === 'css') {
        codeBlock.textContent = `::placeholder {
        color: var(--placeholder);
        opacity: 1;
    }`;
    } else {
        codeBlock.textContent = ''; 
    }

     //_____________________________________________________________________

      //___________________PRISM____________________________________________

    // Trigger syntax highlighting using Prism.js
    Prism.highlightElement(codeBlock);

    // Manage button states
    const buttons = document.querySelectorAll('.language-selector button');
    buttons.forEach(button => button.classList.remove('selected')); // Remove 'selected' class from all buttons

    // Add 'selected' class to the clicked button
    const activeButton = Array.from(buttons).find(button => button.textContent.toLowerCase() === language);
    if (activeButton) {
        console.log('Selected button:', activeButton.textContent); // Debugging
        activeButton.classList.add('selected');
    }
}

    //___________________________________________________________________________________________________________________________________________

    let text; 
    let updateInterval;
    async function fetchFeedback() {
    try {
      //____________________ ERROR BELOW___________________________
      const response = await fetch('/get-feedback');

      //____________________ ERROR BELOW___________________________
      const data = await response.json();
    
      document.getElementById('feedback-text').value = data.feedback || "No feedback yet.";
      text = data.feedback
      
    } 
    
    catch (error) {
      console.error('Error fetching feedback:', error);
    }
  }

  function startFeedbackUpdates() {
    if (updateInterval) {
      clearInterval(updateInterval); // Stop previous interval if any
    }
    fetchFeedback(); // Fetch feedback immediately
    updateInterval = setInterval(fetchFeedback, 5000); // Fetch feedback every 5 seconds
  }

  async function fetch_random_quest() {
    try {
      const response = await fetch('/random-quest');
      const data = await response.json();


      document.getElementById('question-text').value = data.return_question || "No question yet.";
    } catch (error) {
      console.error('Error fetching question:', error);
    }
  }


const pictures = {
    '0':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAx7vYppHG3mDv761hZ7Hn59uGs_JEvPovIk8KEDrdDCnwE35MvIhD8fJ892OWzbkamlQ&usqp=CAU',
    '1': 'https://i.insider.com/5c000abbdde8676422780723?width=800&format=jpeg&auto=webp',
    '2':'https://content.api.news/v3/images/bin/c7373120e827e8fa56d1beb177f4fdee',
    '3':'https://thespun.com/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cfl_progressive%2Cq_auto:good%2Cw_1200/MTgzMTI4MTg5NTc2NTUzODI0/los-angeles-lakers-v-golden-state-warriors.jpg',
    '4':'https://i.pinimg.com/originals/fa/f4/0a/faf40afb241d94b7375bf75ea0d26268.jpg',
    '5':'https://i.imgflip.com/mwhox.jpg',
    '6':'https://cdn.vox-cdn.com/thumbor/jZ8sKeNf5uGO3nN2nzrnNr5yNQQ=/0x40:960x680/1200x800/filters:focal(0x40:960x680)/cdn.vox-cdn.com/uploads/chorus_image/image/10416343/lebronnn.0.jpg',
    '7':'https://hoopshype.com/wp-content/uploads/sites/92/2021/10/i_33_e4_43_lebron-james.png',
    '8':'https://cdn.chatsports.com/cache/eb/0f/eb0f3a1d9bf483c012a6be10acbd6bb5-original.jpg',
    '9':'https://b.thumbs.redditmedia.com/hLCyjXo_FrWZVmuV5jCHKFrqGMEzE4MpQS13t6_5tps.jpg'}






