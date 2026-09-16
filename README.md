# AVA - Assistive Voice Assistant Hardware Robot

AVA is a voice-assistive robot designed to bridge the communication gap between 
disabled and non-disabled individuals. It combines **sign language detection** 
with **NLP** to interpret signed input and generate natural spoken/text responses, 
paired with a **hardware robot** that uses **face and object detection** (YOLOv8) 
to recognize and engage with people in its environment.

This project was built as a BE Major Project with the goal of making everyday 
communication more accessible for people who use sign language.

## Features
- Real-time sign language detection and interpretation
- NLP-based response generation for natural conversation
- Face/object detection using YOLOv8 for environment awareness
- Voice-assistive hardware robot integration

## Tech Stack
- Python
- YOLOv8 (object/face detection)
- Ollama (LLaMA 3) for local LLM inference
- NLP for language processing

## Setup

- Download Ollama: https://ollama.com/download/windows
- Run the model: `ollama run llama3` (in an admin terminal)
- Install the Ollama Python package: `pip install ollama`
- Create a virtual environment: `python -m venv venv`
- Activate it: `.\venv\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`
- Run the full program: `python main.py`

*Note: add `/venv` to `.gitignore` before committing.*
