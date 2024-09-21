import subprocess
import pyttsx3
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import io
from scipy.io.wavfile import write
import platform
import ollama
import signal
import sys

# Initialize the pyttsx3 TTS engine
engine = pyttsx3.init()

# Function to convert text to speech
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Function to record audio using sounddevice
def record_audio(duration=5, sample_rate=16000):
    print("Listening...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    return audio_data, sample_rate

# Function to convert audio data to WAV format for `speech_recognition`
def audio_to_wav(audio_data, sample_rate):
    audio_io = io.BytesIO()
    write(audio_io, sample_rate, np.array(audio_data, dtype='int16'))
    audio_io.seek(0)
    return audio_io

# Function to capture voice input
def get_voice_input():
    recognizer = sr.Recognizer()

    audio_data, sample_rate = record_audio(duration=10)
    audio_io = audio_to_wav(audio_data, sample_rate)

    with sr.AudioFile(audio_io) as source:
        audio = recognizer.record(source)

    try:
        print("Recognizing command...")
        command = recognizer.recognize_google(audio)
        print(f"User said: {command}")
        return command.lower()  # Convert to lowercase for easier matching
    except sr.UnknownValueError:
        speak_text("Sorry, I couldn't understand your voice.")
        return None
    except sr.RequestError:
        speak_text("Sorry, I couldn't reach the speech recognition service.")
        return None

# Object detection process management
object_detection_process = None

# Function to start object detection
def start_object_detection():
    global object_detection_process
    script_path = "object_detection.py"  # Update with the correct path to your object detection script
    
    if object_detection_process is None:
        try:
            if platform.system() == 'Windows':
                object_detection_process = subprocess.Popen(['python', script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
            elif platform.system() == 'Linux':
                object_detection_process = subprocess.Popen(['gnome-terminal', '--', 'python3', script_path])
            elif platform.system() == 'Darwin':  # macOS
                object_detection_process = subprocess.Popen(['osascript', '-e', f'tell application "Terminal" to do script \"python3 {script_path}\"'])
            speak_text("Object detection started.")
        except Exception as e:
            print(f"Error starting object detection: {e}")
            speak_text("Error starting object detection.")
    else:
        speak_text("Object detection is already running.")

# Function to stop object detection
def stop_object_detection():
    global object_detection_process
    if object_detection_process is not None:
        try:
            object_detection_process.terminate()
            object_detection_process.wait()
            object_detection_process = None
            speak_text("Object detection stopped.")
        except Exception as e:
            print(f"Error stopping object detection: {e}")
            speak_text("Error stopping object detection.")
    else:
        speak_text("Object detection is not running.")

# Function to terminate the entire program
def terminate_program():
    if object_detection_process is not None:
        stop_object_detection()  # Ensure object detection is stopped before quitting
    speak_text("Terminating the program. Goodbye!")
    sys.exit()

# Function to handle user commands
def handle_command(command):
    if command is None:
        return

    if "start object detection" in command:
        start_object_detection()
    elif "stop object detection" in command:
        stop_object_detection()
    elif "stop" in command or "terminate" in command or "exit" in command:
        terminate_program()
    else:
        # If it's not a command, handle it as a question to Ollama
        handle_chat(command)

# Function to handle chat with the Ollama model
def handle_chat(question):
    try:
        response = ollama.chat(
            model="llama3",  # Use 'llama3' if available
            messages=[{"role": "user", "content": question}],
        )
        answer = response.get("message", {}).get("content", "Sorry, I couldn't find an answer.")
        print(answer)
        speak_text(answer)
    except Exception as e:
        print(f"Error interacting with Ollama: {e}")
        speak_text("Sorry, there was an issue processing your request.")

# Main logic
def main():
    listening = False

    while True:
        if not listening:
            user_input = input("Enter 'Hey Ava' to start listening for commands: ").strip()
            
            if user_input.lower() == "hey ava":
                speak_text("Listening activated. Say your command.")
                listening = True
            else:
                print("Command not recognized. Please enter 'Hey Ava' to start.")
        else:
            # Get the voice input from the user
            command = get_voice_input()

            if command:
                handle_command(command)

if __name__ == "__main__":
    main()
