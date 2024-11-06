from enum import Enum
from random import choice

# Placeholder imports for feedback_module, context_manager, and learning
import feedback_processor  # Placeholder for feedback processing
import context_manager  # Placeholder for context management
import learning_module  # Placeholder for dynamic response learning (e.g., web scraping)


class EmotionType(Enum):
    """Defines basic emotional states."""
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    CALM = "calm"
    STRESSED = "stressed"
    MOTIVATED = "motivated"
    BORED = "bored"
    NEUTRAL = "neutral"


class EmotionalState:
    """Represents the emotional state of the user."""
    
    def __init__(self, emotion=EmotionType.NEUTRAL, intensity=0.5):
        """
        Initialize with a default emotion and intensity.
        
        Parameters:
        - emotion: EmotionType, default NEUTRAL
        - intensity: float, from 0.0 (low) to 1.0 (high)
        """
        self.emotion = emotion
        self.intensity = intensity  # Scale from 0.0 to 1.0
        
    def update_emotion(self, new_emotion, new_intensity):
        """Updates the emotional state with a new emotion and intensity."""
        self.emotion = new_emotion
        self.intensity = max(0.0, min(new_intensity, 1.0))  # Keep intensity within bounds
    
    def __str__(self):
        return f"Emotion: {self.emotion.value}, Intensity: {self.intensity}"


class EmotionalResponse:
    """Generates nuanced responses based on EmotionalState, feedback, and context awareness, with learning integration."""
    
    # Fallback RESPONSE_MAP if no dynamic response is available
    RESPONSE_MAP = {
        EmotionType.HAPPY: {
            'low': ["I'm glad to see you’re in a good mood!"],
            'medium': ["That's wonderful! Keep up the positive vibes!"],
            'high': ["Your happiness is contagious! Spread the joy!"]
        },
        EmotionType.SAD: {
            'low': ["I'm here for you if you need me."],
            'medium': ["Take your time. I'm here to support you."],
            'high': ["I'm sorry you're feeling down. I'm here to listen anytime."]
        },
        EmotionType.ANGRY: {
            'low': ["It sounds like you’re a bit frustrated. I’m here to help."],
            'medium': ["I'm here if you need to vent or need a break."],
            'high': ["It sounds like you're really upset. Let's work through this together."]
        },
        EmotionType.NEUTRAL: {
            'low': ["How can I assist you today?"],
            'medium': ["I'm ready whenever you are!"],
            'high': ["I'm here, ready and attentive!"]
        }
    }
    
    def get_intensity_level(self, intensity):
        """Categorizes intensity into 'low', 'medium', or 'high'."""
        if intensity < 0.3:
            return 'low'
        elif intensity < 0.7:
            return 'medium'
        else:
            return 'high'
    
    def get_response(self, emotional_state, context=None):
        """
        Generate a nuanced response based on the EmotionalState, context, and dynamic learning.
        
        Parameters:
        - emotional_state: EmotionalState
        - context: Optional; information from context_manager
        
        Returns:
        - str: A response suitable to the detected emotion, intensity, and context.
        """
        intensity_level = self.get_intensity_level(emotional_state.intensity)
        
        # Fetch a dynamic response based on emotion, intensity, and context from learning.py
        dynamic_response = learning.fetch_dynamic_response(
            emotion=emotional_state.emotion, 
            intensity=intensity_level,
            context=context
        )
        
        # Use dynamic response if available, otherwise fall back to predefined map
        if dynamic_response:
            response = dynamic_response
        else:
            base_responses = self.RESPONSE_MAP.get(emotional_state.emotion, {}).get(intensity_level, ["I'm here for you."])
            response = choice(base_responses)
        
        # Modify response based on context if available
        if context:
            response = self.context_aware_response(response, context)
        
        return response

    def context_aware_response(self, response, context):
        """
        Modify the response based on context.
        
        Parameters:
        - response: str, initial response
        - context: dict, context data from context_manager
        
        Returns:
        - str: Contextually aware response.
        """
        # Placeholder for getting context. Replace with actual method calls from context_manager
        context_data = context.get('activity', None)
        if context_data == 'work_stress':
            response += " I noticed you've had a busy schedule lately. Remember to take breaks!"
        elif context_data == 'high_productivity':
            response += " Great job on staying focused today!"
        
        return response

    def receive_feedback(self, emotional_state, response, feedback):
        """
        Adjust future responses based on user feedback.
        
        Parameters:
        - emotional_state: EmotionalState, current user emotion
        - response: str, AI response given
        - feedback: dict, feedback data from feedback_module
        """
        # Process feedback through feedback_module
        feedback_module.process_feedback(emotional_state.emotion, response, feedback)
        
        # Save user-approved responses dynamically in learning module
        if feedback.get('user_reaction') == 'positive':
            learning.save_response(emotional_state.emotion, response, feedback)


# Usage example

# Creating an initial emotional state
user_emotion = EmotionalState(emotion=EmotionType.STRESSED, intensity=0.7)
print(user_emotion)

# Getting a context-aware and intensity-nuanced response with dynamic learning
response_generator = EmotionalResponse()

# Placeholder context example (from context_manager)
context_example = {
    'activity': 'work_stress'
}

response = response_generator.get_response(user_emotion, context=context_example)
print("Assistant Response:", response)

# Placeholder feedback example
feedback_example = {
    'user_reaction': 'positive',  # User liked the response
    'suggestion': None
}

# Processing feedback and saving response dynamically in learning
response_generator.receive_feedback(user_emotion, response, feedback_example)