import cv2
import threading
import queue
import speech_recognition as sr
import google.generativeai as genai

# Global Variables
transcription_queue = queue.Queue()
response_queue = queue.Queue()
stop_threads = False

# API Configuration
GEMINI_API_KEY = "AIzaSyDCp0XLchwdXv1rG3U4wXY85h6CFh_1wBA"
genai.configure(api_key=GEMINI_API_KEY)

# Function to get Gemini response using the Gemini SDK
# Function to get Gemini response with mock interview context
def get_gemini_response(prompt):
    try:
        # Add context to the prompt for mock interview
        interview_context = """
        You are helping a friend with a mock interview. The following text is part of a mock interview. 
        Your task is to provide really short friendly feedback on how your friend can prove their speaking
        """

        # Combine context with the transcription
        full_prompt = interview_context + "\n" + prompt

        # Generate content using Gemini
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(full_prompt, stream = True)

        # Collect the response chunks
        generated_content = ""
        for chunk in response:
            generated_content += chunk.text

        return generated_content

    except Exception as e:
        return f"Error communicating with Gemini API: {e}"


# Video Processing
def video_processing():
    global stop_threads
    cap = cv2.VideoCapture(0)  # Use the first webcam
    cap.set(cv2.CAP_PROP_FPS, 15)  # Limit FPS to 15
    cap.set(3, 640)  # Set frame width to 640
    cap.set(4, 480)  # Set frame height to 480

    while not stop_threads:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Mock Interview Video Feed", frame)

        # Stop on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_threads = True
            break

    cap.release()
    cv2.destroyAllWindows()

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
                audio = recognizer.listen(source, timeout=5)

                transcription = recognizer.recognize_google(audio)
                print(f"Transcription: {transcription}")
                transcription_queue.put(transcription)

        except sr.WaitTimeoutError:
            print("No speech detected. Retrying...")
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except Exception as e:
            print(f"Error during audio transcription: {e}")

# Processing Gemini Responses
def process_gemini_responses():
    global stop_threads
    while not stop_threads:
        try:
            # Wait for a transcription
            transcription = transcription_queue.get(timeout=1)
            print(f"Sending to Gemini: {transcription}")

            # Get Gemini feedback
            feedback = get_gemini_response(transcription)
            response_queue.put(feedback)
            print(f"Gemini Feedback: {feedback}")

        except queue.Empty:
            continue
        except Exception as e:
            print(f"Error processing Gemini response: {e}")

# Display Gemini Feedback
def display_gemini_responses():
    global stop_threads
    while not stop_threads:
        try:
            # Wait for Gemini feedback
            feedback = response_queue.get(timeout=1)
            print(f"\n--- Gemini Feedback ---\n{feedback}\n")

        except queue.Empty:
            continue

# Main Application
if __name__ == "__main__":
    # Create threads for video, audio, Gemini processing, and feedback display
    video_thread = threading.Thread(target=video_processing)
    audio_thread = threading.Thread(target=audio_transcription)
    gemini_thread = threading.Thread(target=process_gemini_responses)
    display_thread = threading.Thread(target=display_gemini_responses)

    try:
        # Start all threads
        video_thread.start()
        audio_thread.start()
        gemini_thread.start()
        display_thread.start()

        # Keep the main thread running until stopped
        while not stop_threads:
            pass

    except KeyboardInterrupt:
        stop_threads = True
        print("Stopping application...")

    # Wait for threads to finish
    video_thread.join()
    audio_thread.join()
    gemini_thread.join()
    display_thread.join()

    print("Application terminated.")
