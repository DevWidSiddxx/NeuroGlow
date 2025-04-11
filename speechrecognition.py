import speech_recognition as sr
import pyttsx3
import requests
import json
import os
import time

class SimpleMoodDetector:
    def __init__(self):
        # Initialize the recognizer
        self.recognizer = sr.Recognizer()
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Adjust speed
        
        print("Simple Mood Detection System initialized successfully!")
        
    def speak(self, text):
        """Text-to-speech output"""
        print(text)
        self.engine.say(text)
        self.engine.runAndWait()
        
    def listen(self):
        """Listen to user input"""
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening... Speak now.")
            try:
                audio = self.recognizer.listen(source, timeout=5)
                return audio
            except sr.WaitTimeoutError:
                print("No speech detected")
                return None
                
    def transcribe(self, audio):
        """Convert speech to text"""
        if not audio:
            return None
            
        try:
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError:
            print("Could not request results from speech recognition service")
            return None
            
    def analyze_mood(self, text):
        """Analyze mood from text using a simple API or rule-based approach"""
        if not text:
            return "neutral"
            
        # Option 1: Text Analysis API (HuggingFace Inference API - no installation needed)
        # This is a free API with rate limits, but works well for simple use cases
        try:
            API_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
            headers = {"Authorization": f"Bearer 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"}
            
            response = requests.post(API_URL, headers=headers, json={"inputs": text})
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    emotions = result[0]
                    # Find emotion with highest score
                    highest_emotion = max(emotions, key=lambda x: x['score'])
                    print(f"API detected mood: {highest_emotion}")
                    
                    # Map to more common terms
                    emotion_mapping = {
                        'joy': 'happy',
                        'sadness': 'sad',
                        'anger': 'angry',
                        'fear': 'fearful',
                        'love': 'loving',
                        'surprise': 'surprised',
                        'neutral': 'neutral'
                    }
                    
                    return emotion_mapping.get(highest_emotion['label'], highest_emotion['label'])
                    
            # Fall back to keyword approach if API fails
            print("API response issue, using fallback approach")
            
        except Exception as e:
            print(f"API error: {e}")
            print("Using fallback keyword-based approach")
        
        # Option 2: Simple keyword-based approach (no API needed)
        text = text.lower()
        
        # Simple word-emotion mapping
        happy_words = ['happy', 'glad', 'joy', 'good', 'great', 'excellent', 'wonderful', 'amazing', 'awesome',
                       'excited', 'love', 'enjoy', 'smile', 'laugh', 'fantastic', 'pleased', 'delighted']
                       
        sad_words = ['sad', 'unhappy', 'depressed', 'down', 'blue', 'upset', 'disappointed', 'miserable',
                    'gloomy', 'heartbroken', 'crying', 'tear', 'sorry', 'regret', 'grief', 'hopeless']
                    
        angry_words = ['angry', 'mad', 'furious', 'annoyed', 'irritated', 'frustrated', 'outraged',
                      'hate', 'rage', 'hostile', 'bitter', 'enraged', 'pissed', 'resentful']
                      
        afraid_words = ['afraid', 'scared', 'fear', 'terrified', 'anxious', 'worried', 'nervous',
                       'panic', 'dread', 'frightened', 'alarmed', 'horrified', 'stressed']
                       
        surprised_words = ['surprised', 'shocked', 'amazed', 'astonished', 'speechless', 'stunned',
                          'unexpected', 'startled', 'wow', 'whoa', 'unbelievable']
        
        # Count word matches
        mood_counts = {
            'happy': sum(word in text for word in happy_words),
            'sad': sum(word in text for word in sad_words),
            'angry': sum(word in text for word in angry_words),
            'afraid': sum(word in text for word in afraid_words),
            'surprised': sum(word in text for word in surprised_words)
        }
        
        # Find mood with highest count, default to neutral if no matches
        max_count = max(mood_counts.values())
        if max_count > 0:
            mood = max(mood_counts.items(), key=lambda x: x[1])[0]
        else:
            mood = 'neutral'
            
        return mood
        
    def get_response(self, mood):
        """Generate appropriate response based on detected mood"""
        responses = {
            'happy': "I can tell you're feeling happy! That's wonderful to hear. What's bringing you joy today?",
            'sad': "I sense that you're feeling sad. It's okay to feel down sometimes. Would you like to share what's on your mind?",
            'angry': "I notice you seem angry or frustrated. Sometimes talking about it can help. What's bothering you?",
            'afraid': "I can tell you're feeling anxious or afraid. Remember to take deep breaths. Would you like to talk about your concerns?",
            'surprised': "You sound surprised! What's unexpected in your day?",
            'neutral': "You sound fairly neutral right now. How has your day been going?",
            'loving': "I sense warmth in your words. It's nice to experience positive feelings like this."
        }
        
        return responses.get(mood, f"I detect that you're feeling {mood}. Would you like to tell me more about how you're feeling?")
    
    def run(self):
        """Main function to run the mood detection system"""
        self.speak("Welcome to the Simple Mood Detection System. I'll listen and tell you what emotion I detect.")
        
        while True:
            self.speak("Please speak about how you're feeling or anything on your mind.")
            
            # Listen for speech
            audio = self.listen()
            if not audio:
                self.speak("I didn't hear anything. Let's try again.")
                continue
                
            # Transcribe speech
            text = self.transcribe(audio)
            if not text:
                self.speak("I couldn't understand what you said. Please try again.")
                continue
                
            # Check for exit commands
            if any(word in text.lower() for word in ["exit", "quit", "stop", "goodbye"]):
                self.speak("Thank you for using the Mood Detection System. Goodbye!")
                break
                
            # Analyze mood
            mood = self.analyze_mood(text)
            
            # Provide feedback
            self.speak(f"Based on what you said, I detect that you're feeling {mood}.")
            
            # Give appropriate response
            response = self.get_response(mood)
            self.speak(response)
            
            # Ask to continue
            self.speak("Would you like to continue? Say yes to continue or goodbye to exit.")
            
            # Listen for response
            audio = self.listen()
            if not audio:
                continue
                
            cont_response = self.transcribe(audio)
            if not cont_response or not any(word in cont_response.lower() for word in ["yes", "yeah", "sure", "continue"]):
                self.speak("Thank you for using the Mood Detection System. Take care!")
                break

if __name__ == "__main__":
    # Create and run the simple mood detector
    detector = SimpleMoodDetector()
    detector.run()
