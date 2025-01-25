function changeLanguage(language) {
    const codeBlock = document.getElementById('codeBlock'); // The <code> block inside the <pre>

    // Remove any existing language classes from the <code> block
    codeBlock.className = ''; // Clear all classes
    codeBlock.classList.add(`language-${language}`); // Add the new language class

    // Update the code content dynamically based on the selected language
    switch (language) {
        case 'java':
            codeBlock.textContent = `public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}`;
            break;
        case 'cpp':
            codeBlock.textContent = `#include <iostream>
using namespace std;

int main() {
    cout << "Hello, World!" << endl;
    return 0;
}`;
            break;
        case 'python':
            codeBlock.textContent = `print("Hello, World!")`;
            break;
        case 'css':
            codeBlock.textContent = `::placeholder {
    color: var(--placeholder);
    opacity: 1;
}`;
            break;
        default:
            codeBlock.textContent = ''; // Default to empty if no language matches
            break;
    }

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
