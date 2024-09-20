import ollama
import pyttsx3
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import io
from scipy.io.wavfile import write

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

    # Record audio for a longer duration to capture the question
    audio_data, sample_rate = record_audio(duration=10)
    audio_io = audio_to_wav(audio_data, sample_rate)

    with sr.AudioFile(audio_io) as source:
        audio = recognizer.record(source)

    try:
        print("Recognizing question...")
        query = recognizer.recognize_google(audio)
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I could not understand your voice.")
        return None
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        return None

# Main logic
def main():
    listening = False

    while True:
        if not listening:
            user_input = input("Enter 'Hey Ava' to start listening for questions: ").strip()
            
            if user_input.lower() == "hey ava":
                print("Listening activated. Say your questions...")
                listening = True
            else:
                print("Command not recognized. Please enter 'Hey Ava' to start.")
        else:
            # Get the voice input from the user
            question = get_voice_input()

            if question:
                # Example of a chat session with ollama
                response = ollama.chat(
                    model="llama3",  # Use 'llama3' if available
                    messages=[{"role": "user", "content": question}],
                )

                # Extract the chatbot's response
                answer = response.get("message", {}).get("content", "Sorry, I couldn't find an answer.")

                # Print the response
                print(answer)

                # Convert the response to speech
                speak_text(answer)

            # Optionally, you could ask if the user wants to continue or stop
            continue_listening = input("Type 'stop' to stop listening or press Enter to continue...").strip().lower()
            if continue_listening == 'stop':
                print("Stopping. Type 'Hey Ava' to start again.")
                listening = False

if __name__ == "__main__":
    main()
