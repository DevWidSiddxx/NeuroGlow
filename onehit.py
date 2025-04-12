import speech_recognition as sr
import pyttsx3
import requests
import json

class SimpleMoodDetector:
    def __init__(self, verbose=False):
        # Initialize the recognizer
        self.recognizer = sr.Recognizer()
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Adjust speed
        
        # Verbose mode for debugging
        self.verbose = verbose
        if self.verbose:
            print("Simple Mood Detection System initialized successfully!")
        
    def speak(self, text):
        """Text-to-speech output"""
        if self.verbose:
            print(text)
        self.engine.say(text)
        self.engine.runAndWait()
        
    def listen(self):
        """Listen to user input once"""
        with sr.Microphone() as source:
            if self.verbose:
                print("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            if self.verbose:
                print("Listening... Speak now.")
            try:
                return self.recognizer.listen(source, timeout=5)
            except sr.WaitTimeoutError:
                if self.verbose:
                    print("No speech detected")
                return None
                
    def transcribe(self, audio):
        """Convert speech to text"""
        if not audio:
            return None
            
        try:
            text = self.recognizer.recognize_google(audio)
            if self.verbose:
                print(f"You said: {text}")
            return text
        except (sr.UnknownValueError, sr.RequestError):
            return None
            
    def analyze_mood(self, text):
        """Analyze mood from text using API with fallback to keywords"""
        if not text:
            return "neutral"
            
        # Try HuggingFace API first
        try:
            API_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
            headers = {"Authorization": "Bearer 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"}
            
            response = requests.post(API_URL, headers=headers, json={"inputs": text})
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    emotions = result[0]
                    highest_emotion = max(emotions, key=lambda x: x['score'])
                    
                    emotion_mapping = {
                        'joy': 'happy',
                        'sadness': 'sad',
                        'anger': 'angry',
                        'fear': 'afraid',
                        'love': 'loving',
                        'surprise': 'surprised',
                        'neutral': 'neutral'
                    }
                    
                    return emotion_mapping.get(highest_emotion['label'], highest_emotion['label'])
                    
        except Exception:
            pass  # Silently fall through to keyword approach
        
        # Keyword-based approach
        text = text.lower()
        
        happy_words = ['happy', 'glad', 'joy', 'good', 'great', 'excellent', 'wonderful', 
                      'amazing', 'awesome', 'excited', 'love', 'enjoy', 'smile', 'laugh']
        sad_words = ['sad', 'unhappy', 'depressed', 'down', 'upset', 'disappointed', 'miserable']
        angry_words = ['angry', 'mad', 'furious', 'annoyed', 'irritated', 'frustrated', 'hate']
        afraid_words = ['afraid', 'scared', 'fear', 'terrified', 'anxious', 'worried', 'nervous']
        surprised_words = ['surprised', 'shocked', 'amazed', 'astonished', 'wow', 'whoa']
        
        mood_counts = {
            'happy': sum(word in text for word in happy_words),
            'sad': sum(word in text for word in sad_words),
            'angry': sum(word in text for word in angry_words),
            'afraid': sum(word in text for word in afraid_words),
            'surprised': sum(word in text for word in surprised_words)
        }
        
        max_count = max(mood_counts.values())
        return max(mood_counts.items(), key=lambda x: x[1])[0] if max_count > 0 else 'neutral'
        
    def get_response(self, mood):
        """Generate appropriate response based on detected mood"""
        responses = {
            'happy': "I can tell you're feeling happy! That's wonderful to hear.",
            'sad': "I sense that you're feeling sad. It's okay to feel down sometimes.",
            'angry': "I notice you seem angry or frustrated. Sometimes talking about it can help.",
            'afraid': "I can tell you're feeling anxious or afraid. Remember to take deep breaths.",
            'surprised': "You sound surprised! What's unexpected in your day?",
            'neutral': "You sound fairly neutral right now. How has your day been going?",
            'loving': "I sense warmth in your words. It's nice to experience positive feelings like this."
        }
        return responses.get(mood, f"I detect that you're feeling {mood}.")
    
    def detect_mood(self):
        """Detect mood in one interaction (returns mood and response)"""
        audio = self.listen()
        if not audio:
            return None, "I didn't hear anything. Please try again."
            
        text = self.transcribe(audio)
        if not text:
            return None, "I couldn't understand what you said. Please try again."
            
        mood = self.analyze_mood(text)
        response = self.get_response(mood)
        return mood, response

if __name__ == "__main__":
    # Example usage
    detector = SimpleMoodDetector(verbose=True)
    mood, response = detector.detect_mood()
    if mood:
        detector.speak(f"I detect that you're feeling {mood}. {response}")
