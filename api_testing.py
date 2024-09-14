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


"""
# Set properties for the voice
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

# Get available voices and set a specific voice (male/female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # 0 for male, 1 for female
"""
