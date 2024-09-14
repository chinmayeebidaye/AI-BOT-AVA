import ollama
import pyttsx3

# Initialize the pyttsx3 TTS engine
engine = pyttsx3.init()


# Function to convert text to speech
def speak_text(text):
    engine.say(text)
    engine.runAndWait()


# Example of a chat session
response = ollama.chat(
    model="llama3",  # Or 'llama3' if available
    messages=[{"role": "user", "content": "Why is the sky blue?"}],
)

# Extract the chatbot's response
answer = response["message"]["content"]

# Print the response
print(answer)

# Convert the response to speech
speak_text(answer)
