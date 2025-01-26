import cv2
import threading
import queue
import speech_recognition as sr
import google.generativeai as genai

# Global Variables
transcription_queue = queue.Queue()
response_queue = queue.Queue()
silence_queue = queue.Queue()
stop_threads = False
feedback_result = None

# API Configuration
GEMINI_API_KEY = "AIzaSyAbQL_FOS902OSSc7XbunDqa1SelwiBcaM"
genai.configure(api_key=GEMINI_API_KEY)

# Function to get Gemini response
def get_gemini_response(prompt):
    try:
        interview_context = """
        You are helping a friend with a mock interview. The following text is part of a mock interview. 
        Your task is to provide really short friendly feedback on how your friend can improve their speaking.
        Start feedback with a score between 0-9. E.g. "8; <feedback>" 
        Please calibrate your score so that the 'average' person interview will score 5.
        """
        full_prompt = interview_context + "\n" + prompt

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(full_prompt, stream=True)

        generated_content = ""
        for chunk in response:
            generated_content += chunk.text

        return generated_content

    except Exception as e:
        return f"Error communicating with Gemini API: {e}"

"""
# Video Processing
def video_processing():
    global stop_threads
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 15)
    cap.set(3, 640)
    cap.set(4, 480)

    while not stop_threads:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Mock Interview Video Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_threads = True
            break

    cap.release()
    cv2.destroyAllWindows()
"""

# Audio Transcription
def audio_transcription():
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
            silence_queue.put(True)
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except Exception as e:
            print(f"Error during audio transcription: {e}")


# Processing Gemini Responses
def process_gemini_responses():
    global stop_threads, feedback_result
    while not stop_threads:
        try:
            transcription = None
            try:
                transcription = transcription_queue.get(timeout=1)
            except queue.Empty:
                pass

            silence_detected = False
            try:
                silence_detected = silence_queue.get_nowait()
            except queue.Empty:
                pass

            if transcription or silence_detected:
                print(f"Sending to Gemini: {transcription}")
                feedback_result = get_gemini_response(transcription or "No input, providing feedback on overall silence.")
                response_queue.put(feedback_result)
                print(f"Gemini Feedback: {feedback_result}")

        except Exception as e:
            print(f"Error processing Gemini response: {e}")

# Display Gemini Feedback
def display_gemini_responses():
    global stop_threads
    while not stop_threads:
        try:
            feedback = response_queue.get(timeout=1)
            print(f"\n--- Gemini Feedback ---\n{feedback}\n")
        except queue.Empty:
            continue

# Main Application
def start_threads():
    global stop_threads
    stop_threads = False

    #video_thread = threading.Thread(target=video_processing)
    audio_thread = threading.Thread(target=audio_transcription)
    gemini_thread = threading.Thread(target=process_gemini_responses)
    display_thread = threading.Thread(target=display_gemini_responses)

    #video_thread.start()
    audio_thread.start()
    gemini_thread.start()
    display_thread.start()

    return "video_thread", audio_thread, gemini_thread, display_thread 

# Function to get the latest feedback
def get_latest_feedback():
    global feedback_result
    return feedback_result
    
if __name__ == "__main__":
    start_threads()


