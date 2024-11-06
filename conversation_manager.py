from context_manager import ContextManager
from feedback_processor import FeedbackModule
from learning_module import LearningModule
from nlp_processing import NLPProcessing
from emotional_analysis import EmotionalState, EmotionalResponse, EmotionType


class ConversationManager:
    def __init__(self):
        self.context_manager = ContextManager()
        self.feedback_processor = FeedbackModule()
        self.learning_module = LearningModule()
        self.nlp_processing = NLPProcessing()
        
        # Initialize emotional state and response generator
        self.user_emotion = EmotionalState()
        self.emotion_response = EmotionalResponse()
    
    def initiate_conversation(self):
        """Start a new conversation, considering the user's initial emotional state."""
        greeting = "Hello! How can I assist you today?"
        context = self.context_manager.get_initial_context()

        # Get an emotion-aware greeting if user has an emotional state
        if self.user_emotion:
            greeting = self.emotion_response.get_response(self.user_emotion, context)
        
        print(greeting)
        return greeting
    
    def process_user_input(self, user_input):
        """
        Process the user's input, analyze emotional cues, and maintain conversation context.
        
        Parameters:
        - user_input: str, input text from user.
        
        Returns:
        - str, generated response considering emotion and context.
        """
        # Update emotional state based on user input analysis
        detected_emotion, intensity = self.nlp_processing.analyze_emotion(user_input)
        self.user_emotion.update_emotion(detected_emotion, intensity)
        
        # Generate response with current emotional context and user input context
        context = self.context_manager.get_context(user_input)
        response = self.emotion_response.get_response(self.user_emotion, context)
        
        print("Assistant Response:", response)
        return response
    
    def conclude_conversation(self):
        """Conclude conversation with an emotion-sensitive goodbye."""
        farewell = "Goodbye! Take care."
        
        # Customize goodbye based on final emotional state
        if self.user_emotion:
            context = self.context_manager.get_context('farewell')
            farewell = self.emotion_response.get_response(self.user_emotion, context)
        
        print(farewell)
        return farewell
    
    def handle_feedback(self, user_feedback):
        """
        Process user feedback to adjust emotional response in future interactions.
        
        Parameters:
        - user_feedback: dict, feedback details such as 'user_reaction'.
        """
        # Log and learn from feedback based on the last emotional response
        self.feedback_module.process_feedback(self.user_emotion.emotion, self.emotion_response, user_feedback)
        if user_feedback.get('user_reaction') == 'positive':
            self.learning_module.save_response(self.user_emotion.emotion, self.emotion_response, user_feedback)
        print("Feedback processed.")

# Example usage:
if __name__ == "__main__":
    cm = ConversationManager()
    cm.initiate_conversation()
    cm.process_user_input("I'm feeling a bit overwhelmed with work.")
    cm.handle_feedback({'user_reaction': 'positive', 'suggestion': None})
    cm.conclude_conversation()