import speech_recognition as sr
import re

class EmotionWordDetector:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    def listen_once(self):
        """Listen one time and return emotion words"""
        with sr.Microphone() as source:
            print("\nAdjusting for ambient noise... (1 second)")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Speak now (I'll listen for 5 seconds max)...")
            
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio)
                print(f"\nYou said: {text}")
                return self.extract_emotion_words(text)
                
            except sr.WaitTimeoutError:
                print("No speech detected")
                return []
            except sr.UnknownValueError:
                print("Could not understand audio")
                return []
            except sr.RequestError:
                print("Could not contact speech service")
                return []
    
    def extract_emotion_words(self, text):
        """Extract emotion words from text (one-time)"""
        emotion_words = {
            'happy': ['happy', 'joy', 'joyful', 'glad', 'delighted', 'pleased', 'cheerful'],
            'sad': ['sad', 'unhappy', 'depressed', 'depressing', 'miserable', 'gloomy'],
            'angry': ['angry', 'mad', 'furious', 'annoyed', 'frustrated', 'irritated'],
            'fearful': ['afraid', 'scared', 'fearful', 'terrified', 'anxious', 'nervous'],
            'surprised': ['surprised', 'shocked', 'amazed', 'astonished', 'startled']
        }
        
        found_words = []
        for words in emotion_words.values():
            for word in words:
                if re.search(rf'\b{word}\b', text, re.IGNORECASE):
                    found_words.append(word.lower())
        return list(set(found_words))

if __name__ == "__main__":
    print("=== Emotion Word Detector ===")
    print("I'll listen once and tell you which emotion words you used.\n")
    
    detector = EmotionWordDetector()
    emotion_words = detector.listen_once()
    
    if emotion_words:
        print("\nDetected emotion words:")
        for word in emotion_words:
            print(f"- {word}")
    else:
        print("\nNo emotion words detected.")
    
    print("\nProgram ended. Run me again to analyze more speech!")
