from context_manager import ContextManager
from feedback_processor import process_feedback, save_positive_response  # Directly import necessary functions
from learning_module import fetch_dynamic_response, save_response, adapt_response_patterns, train_from_feedback
from nlp_processing import NLPProcessing
from emotional_analysis import EmotionalState, EmotionalAnalysis  # Use EmotionalAnalysis instead of EmotionalResponse
from shared_types import EmotionType

class ConversationManager:
    def __init__(self):
        self.context_manager = ContextManager()
        self.nlp_processing = NLPProcessing()
        
        # Initialize emotional state and response generator
        self.user_emotion = EmotionalState()
        self.emotion_response = EmotionalAnalysis()  # Updated to use EmotionalAnalysis
    
    def initiate_conversation(self):
        """Start a new conversation, considering the user's initial emotional state."""
        greeting = "Hello! How can I assist you today?"
        context = self.context_manager.get_initial_context()

        # Get an emotion-aware greeting if user has an emotional state
        if self.user_emotion:
            greeting = self.emotion_response.get_response(context)
        
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
        response = self.emotion_response.get_response(context)
        
        print("Assistant Response:", response)
        return response
    
    def conclude_conversation(self):
        """Conclude conversation with an emotion-sensitive goodbye."""
        farewell = "Goodbye! Take care."
        
        # Customize goodbye based on final emotional state
        if self.user_emotion:
            context = self.context_manager.get_context('farewell')
            farewell = self.emotion_response.get_response(context)
        
        print(farewell)
        return farewell
    
    def handle_feedback(self, user_feedback):
        """
        Process user feedback to adjust emotional response in future interactions.
        
        Parameters:
        - user_feedback: dict, feedback details such as 'user_reaction'.
        """
        # Log and learn from feedback based on the last emotional response
        process_feedback(self.user_emotion.emotion, self.emotion_response, user_feedback)
        if user_feedback.get('user_reaction') == 'positive':
            save_positive_response(self.user_emotion.emotion, self.emotion_response)
        
        # Optionally adapt response patterns or train from feedback
        adapt_response_patterns()
        train_from_feedback()
        
        print("Feedback processed.")

# Example usage:
if __name__ == "__main__":
    cm = ConversationManager()
    cm.initiate_conversation()
    cm.process_user_input("I'm feeling a bit overwhelmed with work.")
    cm.handle_feedback({'user_reaction': 'positive', 'suggestion': None})
    cm.conclude_conversation()