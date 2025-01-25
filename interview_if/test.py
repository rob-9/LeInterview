import cv2
import threading
import queue
import speech_recognition as sr
import google.generativeai as genai
import time  # Import the time module

# Global Variables
transcription_queue = queue.Queue()
response_queue = queue.Queue()
silence_queue = queue.Queue()  # Queue to handle silence signals
stop_threads = False
feedback_result = None  # Global variable to store the feedback result

# API Configuration
GEMINI_API_KEY = "AIzaSyDCp0XLchwdXv1rG3U4wXY85h6CFh_1wBA"
genai.configure(api_key=GEMINI_API_KEY)


# Function to get Gemini response with mock interview context
def get_gemini_response(prompt):
    try:
        interview_context = """
        You are helping a friend with a mock interview. The following text is part of a mock interview. 
        Your task is to provide really short friendly feedback on how your friend can improve their speaking.
        """
        full_prompt = interview_context + "\n" + prompt

        # Generate content using Gemini
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(full_prompt, stream=True)

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

                # Listen for audio with a timeout to detect silence
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                transcription = recognizer.recognize_google(audio)
                print(f"Transcription: {transcription}")
                transcription_queue.put(transcription)

        except sr.WaitTimeoutError:
            print("Silence detected for 5 seconds.")
            silence_queue.put(True)  # Signal silence
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except Exception as e:
            print(f"Error during audio transcription: {e}")


# Processing Gemini Responses
def process_gemini_responses():
    global stop_threads, feedback_result
    while not stop_threads:
        try:
            # Wait for a silence signal or transcription
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

            # Trigger feedback if silence detected or transcription available
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
def main():
    global stop_threads, feedback_result
    video_thread = threading.Thread(target=video_processing)
    audio_thread = threading.Thread(target=audio_transcription)
    gemini_thread = threading.Thread(target=process_gemini_responses)
    display_thread = threading.Thread(target=display_gemini_responses)

    try:
        video_thread.start()
        audio_thread.start()
        gemini_thread.start()
        display_thread.start()

        # Run the main loop for 10 seconds
        start_time = time.time()
        while time.time() - start_time < 10:
            pass
        stop_threads = True  # Signal all threads to stop

    except KeyboardInterrupt:
        stop_threads = True
        print("Stopping application...")

    # Wait for threads to finish
    video_thread.join()
    audio_thread.join()
    gemini_thread.join()
    display_thread.join()

    print("Application terminated.")
    return feedback_result  # Return the last feedback generated


if __name__ == "__main__":
    result = main()
    print(f"Final Feedback: {result}")


