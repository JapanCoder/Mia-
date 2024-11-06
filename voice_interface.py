import speech_recognition as sr
import pyttsx3
import threading
import time
from error_logger import ErrorLogger  # Assuming we have an error logger module
from task_scheduler import TaskScheduler  # For queued responses if needed

class VoiceInterface:
    def __init__(self):
        # Initialize recognizer and TTS engine
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self.logger = ErrorLogger()
        self.task_scheduler = TaskScheduler()
        
        # Customizable TTS settings
        self.voice_speed = 150  # Default speed for TTS
        self.voice_volume = 0.9  # Default volume level for TTS
        self._configure_tts()

        # State management
        self.listening = False  # Indicates if Mia is listening for commands
        self.response_queue = []  # Queue to store responses for sequential output

    def _configure_tts(self):
        """Configures TTS settings like speed, volume, and voice."""
        self.tts_engine.setProperty('rate', self.voice_speed)
        self.tts_engine.setProperty('volume', self.voice_volume)
        
        # Optionally, set a specific voice (e.g., female/male)
        voices = self.tts_engine.getProperty('voices')
        self.tts_engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)

    def listen(self) -> str:
        """Continuously listens for voice input and converts it to text."""
        with sr.Microphone() as source:
            print("Mia is listening...")
            self.listening = True
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                user_input = self.recognizer.recognize_google(audio)
                print(f"User said: {user_input}")
                return user_input
            except sr.WaitTimeoutError:
                self.logger.log_error("Voice timeout: No input detected.")
                return "timeout"
            except sr.UnknownValueError:
                self.logger.log_error("Voice recognition error: Could not understand audio.")
                return "unintelligible"
            except sr.RequestError as e:
                self.logger.log_error(f"Voice service error: {e}")
                return "error"
            finally:
                self.listening = False

    def speak(self, text: str):
        """Converts text to speech output and manages queued responses."""
        if not text:
            self.logger.log_error("Attempted to speak empty text.")
            return
        
        # If the engine is speaking, queue the new response
        if self.tts_engine._inLoop:
            self.response_queue.append(text)
        else:
            # Otherwise, speak immediately
            print("Mia says:", text)
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            self._process_response_queue()

    def _process_response_queue(self):
        """Processes any responses queued while TTS engine was busy."""
        while self.response_queue:
            next_response = self.response_queue.pop(0)
            self.tts_engine.say(next_response)
            self.tts_engine.runAndWait()

    def set_voice_speed(self, speed: int):
        """Sets the TTS speed."""
        self.voice_speed = speed
        self.tts_engine.setProperty('rate', speed)

    def set_voice_volume(self, volume: float):
        """Sets the TTS volume level."""
        if 0.0 <= volume <= 1.0:
            self.voice_volume = volume
            self.tts_engine.setProperty('volume', volume)
        else:
            self.logger.log_error("Invalid volume level. Must be between 0.0 and 1.0.")

    def start_conversation(self):
        """Starts a voice-based conversation loop."""
        print("Voice interface activated. Start speaking...")
        while True:
            user_input = self.listen()
            if user_input in ["timeout", "unintelligible", "error"]:
                self.speak("I didn't catch that. Could you please repeat?")
                continue

            # Process the user's command (this would involve routing to CommandParser)
            response = self.process_command(user_input)  # Placeholder function
            self.speak(response)

            # Break the conversation loop on specific keywords
            if user_input.lower() in ["stop", "goodbye", "exit"]:
                self.speak("Goodbye! Talk to you soon.")
                break

    def process_command(self, user_input: str) -> str:
        """
        Placeholder for command processing logic.
        Here, we'd integrate with CommandParser to interpret and respond to user input.
        """
        # Example response for demonstration
        return f"I understood you said: '{user_input}'. How else can I assist?"

# Example usage
if __name__ == "__main__":
    voice_interface = VoiceInterface()
    voice_interface.start_conversation()