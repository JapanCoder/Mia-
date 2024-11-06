from random import choice
import re
import feedback_processor
import context_manager
import learning_module
from shared_types import EmotionType

class EmotionalState:
    """Represents the emotional state of the user."""
    
    def __init__(self, emotion=EmotionType.NEUTRAL, intensity=0.5):
        self.emotion = emotion
        self.intensity = intensity
    
    def update_emotion(self, new_emotion, new_intensity):
        self.emotion = new_emotion
        self.intensity = max(0.0, min(new_intensity, 1.0))  # Keep intensity within bounds

    def __str__(self):
        return f"Emotion: {self.emotion.value}, Intensity: {self.intensity}"


class EmotionalAnalysis:
    """Analyzes and manages emotional states, context awareness, and feedback-based learning."""

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
        },
        # Added responses for FEARFUL
        EmotionType.FEARFUL: {
            'low': ["It's okay to feel a bit scared. I'm here with you."],
            'medium': ["I can sense you're worried. Let's go through this together."],
            'high': ["I know things may seem frightening, but I'll be here for support."]
        },
        # Added responses for SURPRISED
        EmotionType.SURPRISED: {
            'low': ["Oh! It seems something unexpected happened."],
            'medium': ["Wow, that sounds surprising!"],
            'high': ["That's astonishing! Tell me more."]
        }
    }

    # Emotion keywords for detecting emotions in user input
    emotion_keywords = {
        EmotionType.HAPPY: ["happy", "joy", "glad", "excited", "pleased"],
        EmotionType.SAD: ["sad", "unhappy", "sorrow", "depressed", "down"],
        EmotionType.ANGRY: ["angry", "mad", "frustrated", "upset", "furious"],
        EmotionType.FEARFUL: ["afraid", "scared", "fearful", "worried", "anxious"],
        EmotionType.SURPRISED: ["surprised", "shocked", "amazed", "astonished", "startled"],
    }

    def __init__(self):
        self.current_state = EmotionalState()

    def detect_emotion(self, user_input):
        """
        Detects emotion from user input based on predefined keywords.
        
        Args:
        - user_input (str): The user's input message.
        
        Returns:
        - EmotionType: Detected emotion or NEUTRAL if no emotion is detected.
        """
        user_input = user_input.lower()

        for emotion, keywords in self.emotion_keywords.items():
            if any(re.search(rf"\b{keyword}\b", user_input) for keyword in keywords):
                return emotion

        return EmotionType.NEUTRAL  # Default to NEUTRAL if no keywords are matched

    def get_intensity_level(self, intensity):
        if intensity < 0.3:
            return 'low'
        elif intensity < 0.7:
            return 'medium'
        else:
            return 'high'
    
    def analyze_emotion(self, text):
        detected_emotion = self.detect_emotion(text)
        intensity = 0.7 if "very" in text or "extremely" in text else 0.5  # Adjust intensity based on input
        self.current_state.update_emotion(detected_emotion, intensity)
        return self.current_state

    def get_response(self, context=None):
        intensity_level = self.get_intensity_level(self.current_state.intensity)
        dynamic_response = learning_module.fetch_dynamic_response(
            emotion=self.current_state.emotion,
            intensity=intensity_level,
            context=context.get('activity', 'general') if context else 'general'
        )

        if dynamic_response:
            response = dynamic_response
        else:
            base_responses = self.RESPONSE_MAP.get(self.current_state.emotion, {}).get(intensity_level, ["I'm here for you."])
            response = choice(base_responses)
        
        if context:
            response = self.context_aware_response(response, context)
        
        return response

    def context_aware_response(self, response, context):
        context_data = context.get('activity', None)
        if context_data == 'work_stress':
            response += " I noticed you've had a busy schedule lately. Remember to take breaks!"
        elif context_data == 'high_productivity':
            response += " Great job on staying focused today!"
        
        return response

    def update_emotion(self, emotion, intensity):
        self.current_state.update_emotion(emotion, intensity)

    def receive_feedback(self, response, feedback):
        feedback_processor.process_feedback(self.current_state.emotion, response, feedback)
        
        if feedback.get('user_reaction') == 'positive':
            learning_module.save_response(self.current_state.emotion, response, feedback)

# Usage example

# Create EmotionalAnalysis instance
emotional_analysis = EmotionalAnalysis()

# Placeholder context example
context_example = {
    'activity': 'work_stress'
}

# Analyze and update emotion based on text
user_input = "I feel really happy with how things are going!"
emotional_analysis.analyze_emotion(user_input)

# Generate response
response = emotional_analysis.get_response(context=context_example)
print("Assistant Response:", response)

# Placeholder feedback example
feedback_example = {
    'user_reaction': 'positive',
    'suggestion': None
}

# Process feedback
emotional_analysis.receive_feedback(response, feedback_example)