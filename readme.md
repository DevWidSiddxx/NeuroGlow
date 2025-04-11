Simple Mood Detection System

This is a voice based mood detection system built using Python. It listens to your voice input analyzes your emotions and gives appropriate responses. It uses both API based and keyword based techniques for mood detection.

Features

- Voice to text transcription using Google Speech Recognition
- Mood analysis using HuggingFace emotion detection API
- Fallback keyword based mood detection if API is unavailable
- Text to speech responses using pyttsx3
- Understands common moods like happy sad angry afraid surprised and neutral
- Conversational flow with option to continue or exit

Requirements

Make sure you have the following Python libraries installed

- speechrecognition
- pyttsx3
- requests
- pyaudio

You can install them using pip

pip install speechrecognition pyttsx3 requests pyaudio

Note pyaudio may require additional system level setup depending on your operating system

How It Works

1 The system welcomes the user and listens to their voice

2 It converts the voice to text using Google Speech Recognition

3 The text is sent to the HuggingFace API for emotion detection

4 If the API fails a keyword based fallback method is used

5 Based on the detected mood the system responds with empathy

6 The user can choose to continue or exit the conversation

Usage

To run the program simply execute the Python script

python mood_detector.py

Speak into the microphone when prompted and wait for the system to respond

Supported Emotions

- Happy
- Sad
- Angry
- Afraid
- Surprised
- Neutral
- Loving

Notes

- Ensure your microphone is connected and working properly
- The API key used in the script has usage limits and may require updating
- You can expand the keyword dictionary to improve offline accuracy
- This project is ideal for mental health awareness chatbot and educational demos

Acknowledgments

- HuggingFace for the emotion detection model
- Google Speech Recognition for transcription
- pyttsx3 for text to speech output
