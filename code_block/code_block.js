function changeLanguage(language) {
    const codeBlock = document.getElementById('codeBlock');
    
    // Remove any previous language class
    codeBlock.classList.remove('language-java', 'language-cpp', 'language-python');
    
    // Add the selected language class
    codeBlock.classList.add(`language-${language}`);
    
    // You can also change the default code block for each language
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
    }

    // Apply syntax highlighting
    Prism.highlightElement(codeBlock);
}
