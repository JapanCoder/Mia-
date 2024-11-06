import json
import os
from datetime import datetime
from collections import defaultdict

# Storage file for feedback history
FEEDBACK_FILE = "feedback_data.json"

# Internal storage for feedback
_feedback_data = defaultdict(list)

# --- Helper Functions ---

def load_feedback():
    """Loads previous feedback data for session continuity."""
    global _feedback_data
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            _feedback_data = json.load(f)
    else:
        _feedback_data = defaultdict(list)

def save_feedback():
    """Saves feedback data for future analysis and improvement."""
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(_feedback_data, f)

def timestamp():
    """Returns the current timestamp for feedback entries."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# --- Core Feedback Functions ---

def process_feedback(emotion, response, feedback):
    """
    Processes feedback, categorizes it, and updates learning metrics.
    
    Args:
    - emotion (EmotionType): The emotion that the user was feeling.
    - response (str): The AI response to which feedback was given.
    - feedback (dict): User feedback data (e.g., reaction, specific suggestions).
    """
    feedback_entry = {
        "timestamp": timestamp(),
        "emotion": emotion.value,
        "response": response,
        "reaction": feedback.get("user_reaction", "neutral"),
        "suggestion": feedback.get("suggestion")
    }
    _feedback_data[emotion.value].append(feedback_entry)

    # Update metrics or save positive responses for future use if the reaction is positive
    if feedback_entry["reaction"] == "positive":
        save_positive_response(emotion, response)

    # Optionally, trigger learning updates based on negative or constructive feedback
    if feedback_entry["reaction"] in ["negative", "constructive"]:
        refine_response_strategy(emotion, feedback.get("suggestion"))

    # Save feedback for future reference
    save_feedback()


def save_positive_response(emotion, response):
    """
    Adds highly-rated responses to a repository for use in dynamic response generation.
    
    Args:
    - emotion (EmotionType): The emotion associated with the response.
    - response (str): The response that received positive feedback.
    """
    # Placeholder for saving dynamic responses to a learning module or database
    # Here, you could call `learning.save_response(emotion, response)`
    print(f"Saving positive response for {emotion}: '{response}'")


def refine_response_strategy(emotion, suggestion=None):
    """
    Adjusts response strategies based on constructive feedback or suggestions.
    
    Args:
    - emotion (EmotionType): The emotional context for response refinement.
    - suggestion (str): User-provided suggestion for improving responses.
    """
    # Placeholder for advanced learning, can adjust NLP or sentiment logic dynamically
    if suggestion:
        print(f"Refining response strategy for {emotion} based on suggestion: '{suggestion}'")
    else:
        print(f"Refining response strategy for {emotion} without specific suggestions")


# --- Feedback Analysis Functions ---

def analyze_feedback_trends():
    """
    Analyzes past feedback to identify improvement opportunities.
    
    Returns:
    - dict: Summary of feedback trends, including frequently requested changes.
    """
    trend_summary = {"positive": 0, "neutral": 0, "negative": 0, "common_suggestions": defaultdict(int)}
    
    for emotion, entries in _feedback_data.items():
        for entry in entries:
            trend_summary[entry["reaction"]] += 1
            if entry["suggestion"]:
                trend_summary["common_suggestions"][entry["suggestion"]] += 1
    
    # Convert common suggestions dictionary to a sorted list of tuples
    trend_summary["common_suggestions"] = sorted(trend_summary["common_suggestions"].items(), 
                                                 key=lambda x: x[1], reverse=True)
    return trend_summary


def suggest_improvements():
    """
    Provides specific suggestions to improve Mia’s responses based on feedback trends.
    
    Returns:
    - list: Recommended improvements or adjustments to response strategies.
    """
    trends = analyze_feedback_trends()
    improvements = []

    # Example suggestions based on trends
    if trends["negative"] > trends["positive"]:
        improvements.append("Consider re-evaluating responses for emotional sensitivity.")

    if trends["common_suggestions"]:
        improvements.append(f"Most requested adjustment: {trends['common_suggestions'][0][0]}")
    
    return improvements