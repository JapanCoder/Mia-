# main.py

from mia import Mia
from voice_interface import VoiceInterface
import session_manager
import datetime
import traceback

class MainApp:
    def __init__(self):
        self.mia = Mia()
        self.session_manager = SessionManager()
        self.voice_interface = VoiceInterface()
        self.use_voice = False  # Start in text mode by default
        self.voice_activated = False  # Track if voice activation is triggered

    def run(self):
        """
        Main loop for running Mia in interactive mode.
        Mia will use text-based responses until a command switches to voice mode.
        """
        self.greet_user()
        
        while True:
            user_input = self.get_user_input()

            if user_input.lower() == 'exit':
                self.shutdown()
                break

            elif user_input.lower() == 'switch to voice':
                self.use_voice = True
                self.respond("Voice mode activated. Mia will now respond with voice.")

            elif user_input.lower() == 'switch to text':
                self.use_voice = False
                self.respond("Text mode activated. Mia will now respond with text.")

            elif user_input.lower() == 'help':
                self.show_help()
                
            else:
                response = self.process_input(user_input)
                self.respond(response)

    def greet_user(self):
        """
        Provides a time-based greeting to the user.
        """
        current_hour = datetime.datetime.now().hour
        greeting = "Good evening" if current_hour >= 18 else "Good afternoon" if current_hour >= 12 else "Good morning"
        self.respond(f"{greeting}! Welcome to Mia. Type 'help' for commands or 'switch to voice' to enable voice mode.")
        
    def get_user_input(self) -> str:
        """
        Captures user input, listening for activation if in voice mode.
        """
        if self.use_voice and not self.voice_activated:
            print("Listening for activation keyword... (say 'Hey Mia')")
            input_text = self.voice_interface.listen_for_keyword("Hey Mia")
            self.voice_activated = bool(input_text)
        if self.voice_activated or not self.use_voice:
            self.voice_activated = False  # Reset after activation
            return input("You: ").strip() if not self.use_voice else self.voice_interface.listen()
        
    def process_input(self, user_input: str) -> str:
        """
        Processes the user's input through Mia, with error handling.
        """
        try:
            if not self.session_manager.is_active_session():
                self.session_manager.start_session()

            response = self.mia.process_input(user_input)
            self.session_manager.log_interaction(user_input, response)
            self.collect_feedback()

            return response
        except Exception as e:
            print("An error occurred. Please try again.")
            print(traceback.format_exc())
            return "I'm sorry, something went wrong. Can you please try again?"

    def respond(self, response: str):
        """
        Delivers Mia's response in the current mode (text or voice).
        """
        if self.use_voice:
            self.voice_interface.speak(response)
        else:
            print(f"Mia: {response}")

    def show_help(self):
        """
        Displays a help message with available commands.
        """
        help_message = """
        Here are some commands you can use:
        - 'switch to voice' / 'switch to text': Toggle between voice and text modes
        - 'exit': Exit the application
        - 'help': Show this help message
        - You can ask Mia general questions, request definitions, schedule tasks, and more.
        """
        self.respond(help_message)

    def collect_feedback(self):
        """
        Asks the user for feedback after interactions to improve Mia's responses.
        """
        feedback = input("Was Mia's response helpful? (yes/no): ").strip().lower()
        if feedback == 'yes':
            self.mia.feedback_processor.process_feedback({"feedback": "positive"})
            self.respond("Thank you for your feedback!")
        elif feedback == 'no':
            self.mia.feedback_processor.process_feedback({"feedback": "negative"})
            self.respond("Thank you. I'll work on improving.")

    def shutdown(self):
        """
        Handles the shutdown sequence, including session cleanup.
        """
        self.respond("Goodbye! Shutting down Mia.")
        self.session_manager.end_session()

if __name__ == "__main__":
    app = MainApp()
    app.run()