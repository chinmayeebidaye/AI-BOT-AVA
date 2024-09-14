import ollama

# Example of a chat session
response = ollama.chat(
    model="llama3",  # Or 'llama3' if available in your setup
    messages=[{"role": "user", "content": 'no of words in "hello world as "'}],
)

# Print the response
print(response["message"]["content"])
