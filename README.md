# AI Interview Assistant

## Ideation  
Within the tech industry, securing internships and job-offers often require applicants to pass rigorous screenings in the form of technical and behavioral interviews. And often times, these interviews test niche skills that can be difficult to prepare well for. To address this problem, we created **LeInterview**. This platform places the user into a working coding environment, where they will answer company-specific LeetCode questions. Simultaneously, our algorithm will assess the user's performance and provide real-time feedback. We believe consistent simulation of real interview scenarios will effectively prepare our users for their tech interviews.

---

## Key Features
1. Finds most applicable interview questions, tailored to user's specific company by scraping datasets.
2. Provides a working coding environment, although debugging tools have not yet been added.
3. Uses voice and video to provide real-time feedback on your interview.
4. Adds a unique twist that makes practice more engaging and memorable.

---

## Tech Stack
- **Frontend**: HTML, CSS, and JavaScript for UI.
- **Backend**: Python for processing and logic.  

How it works:  
1. The program scrapes data about the specified company to generate accurate interview questions using **Google Gemini**.  
2. During the interview, the tool transcribes audio in real-time using the **speech_recognition** library in Python.  
3. The transcribed text is sent to the **Google Gemini API** to generate feedback.  
4. We used the **Flask** library to connect the Python backend to the HTML frontend.  

---

## Challenges
1. **Backend Integration**: We initially planned to use **py-script** for Python integration but encountered numerous errors, forcing us to find an alternative solution.  
2. **Frontend Complexity**: Integrating a code interpreter into the website posed significant challenges during development.  

---

## What we learned
This project allowed us to:  
- Explore and utilize various **Python libraries** for backend development.  
- Gain foundational knowledge in **frontend development** using HTML, CSS, and JavaScript.  
- Improve our problem-solving skills by overcoming integration challenges.  

---

## What's next for LeInterview
Our vision is to refine and scale **LeInterview** to help inspire countless students to prepare for interviews with confidence. We aim to:  
- Enhance the accuracy and depth of feedback.  
- Expand the database of company-specific questions.  
- Improve the user interface for a seamless experience.

