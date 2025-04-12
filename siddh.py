import speech_recognition as sr
import pyttsx3
import re

class EmotionVoiceBot:
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        
        # Initialize text-to-speech
        self.engine = pyttsx3.init()
        self.setup_voice()
        
        # Emotion configuration
        self.emotion_keywords = {
            'happy': ['happy', 'joy', 'excited', 'great', 'wonderful', 'awesome'],
            'sad': ['sad', 'depressed', 'unhappy', 'miserable', 'gloomy', 'heartbroken'],
            'angry': ['angry', 'mad', 'furious', 'annoyed', 'frustrated', 'irritated'],
            'anxious': ['anxious', 'nervous', 'stressed', 'worried', 'tense', 'scared'],
        }
        
        # Activity suggestions
        self.suggestions = {
            'happy': [
                "It's wonderful that you're feeling happy!",
                "To maintain this good mood:",
                "1. Share your joy with someone else",
                "2. Do something creative",
                "3. Take a moment to appreciate this feeling",
                "4. Spread positivity by complimenting someone"
            ],
            'sad': [
                "I'm sorry you're feeling down.",
                "Here are some things that might help:",
                "1. Talk to someone you trust",
                "2. Listen to uplifting music",
                "3. Take a walk in nature",
                "4. Write down your thoughts in a journal",
                "Remember: this feeling will pass."
            ],
            'angry': [
                "Anger is a natural emotion, but let's channel it positively:",
                "1. Take 5 deep breaths (inhale 4s, exhale 6s)",
                "2. Go for a brisk walk or run",
                "3. Write down what's bothering you then tear it up",
                "4. Listen to calming music",
                "5. Remind yourself you're in control of your reactions"
            ],
            'anxious': [
                "When feeling anxious, try these techniques:",
                "1. Practice 4-7-8 breathing (inhale 4s, hold 7s, exhale 8s)",
                "2. Focus on your senses - name 5 things you can see",
                "3. Drink some warm tea and sit quietly",
                "4. Do a simple task to distract your mind",
                "You've gotten through anxious moments before - you can do it again."
            ],
            'default': [
                "Here are some general mood boosters:",
                "1. Listen to your favorite song",
                "2. Stretch your body",
                "3. Drink some water",
                "4. Call a friend",
                "5. Do one small thing you've been putting off"
            ]
        }

    def setup_voice(self):
        """Configure voice properties"""
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)  # 0 for male, 1 for female
        self.engine.setProperty('rate', 150)  # Speaking speed

    def speak(self, text):
        """Convert text to speech"""
        print(f"BOT: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """Listen to user input through microphone"""
        with sr.Microphone() as source:
            print("\nAdjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            self.speak("Please speak now - I'm listening for 5 seconds")
            print("Listening...")
            
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text.lower()
                
            except sr.WaitTimeoutError:
                self.speak("I didn't hear anything. Please try again.")
                return None
            except sr.UnknownValueError:
                self.speak("Sorry, I couldn't understand that. Could you repeat?")
                return None
            except sr.RequestError:
                self.speak("There was an error with the speech service. Please check your connection.")
                return None

    def detect_emotion(self, text):
        """Detect emotion from spoken text"""
        if not text:
            return None
            
        for emotion, keywords in self.emotion_keywords.items():
            if any(keyword in text for keyword in keywords):
                return emotion
        return 'neutral'

    def get_suggestions(self, emotion):
        """Get appropriate suggestions based on detected emotion"""
        return self.suggestions.get(emotion, self.suggestions['default'])

    def run(self):
        """Main program loop"""
        self.speak("Welcome to your Emotion Assistant!")
        self.speak("I'll listen to how you're feeling and suggest ways to improve your mood.")
        
        while True:
            # Listen to user
            user_text = self.listen()
            if not user_text:
                continue
                
            # Detect emotion
            emotion = self.detect_emotion(user_text)
            self.speak(f"I sense you're feeling {emotion}.")
            
            # Provide suggestions
            suggestions = self.get_suggestions(emotion)
            for line in suggestions:
                self.speak(line)
            
            # Ask to continue
            self.speak("\nWould you like to talk more about how you're feeling?")
            user_text = self.listen()
            if not user_text or 'no' in user_text:
                self.speak("Okay, take care of yourself! Goodbye.")
                break

if __name__ == "__main__":
    bot = EmotionVoiceBot()
    bot.run()
