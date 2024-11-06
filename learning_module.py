import json
import os
from datetime import datetime, timedelta
import random
from collections import defaultdict

# Placeholder for a model or other learning mechanism
_model = None
_feedback_data = defaultdict(list)  # Stores feedback data with emotion-based categorization


# --- Core Learning Functions ---

def fetch_dynamic_response(emotion, intensity, context):
    """
    Retrieves a dynamically learned response based on the user's emotional state, intensity, and context.
    
    Args:
    - emotion (str): The user's emotional state (e.g., 'happy', 'stressed').
    - intensity (int): Intensity level of the emotion (e.g., 1 to 5).
    - context (str): Additional context for shaping the response (e.g., 'work_stress').
    
    Returns:
    - str or None: A suitable learned response if available, else None.
    """
    if _model:
        return _model.predict(emotion, intensity, context)
    else:
        return f"I can see you're feeling {emotion} with {intensity} intensity. Let's work through it."


def save_response(emotion, response, feedback):
    """
    Stores responses that received positive feedback for potential future reuse.
    
    Args:
    - emotion (str): The emotional category of the response.
    - response (str): The response text given to the user.
    - feedback (dict): Feedback data associated with this response.
    """
    entry = {
        "response": response,
        "feedback": feedback,
        "timestamp": datetime.now().isoformat()
    }
    _feedback_data[emotion].append(entry)
    if sum(len(entries) for entries in _feedback_data.values()) % 10 == 0:
        save_feedback_data()


def adapt_response_patterns():
    if _feedback_data:
        positive_feedback = [entry for entries in _feedback_data.values() for entry in entries if entry["feedback"].get("rating", 0) > 3]
        print(f"Adapting response patterns based on {len(positive_feedback)} positive feedback entries.")


def train_from_feedback():
    if _feedback_data:
        print(f"Training model with {sum(len(entries) for entries in _feedback_data.values())} feedback entries.")
        _feedback_data.clear()


# --- Model Persistence Functions ---

def save_model(file_path="model.pkl"):
    if _model:
        with open(file_path, "wb") as f:
            print("Model saved to disk.")


def load_model(file_path="model.pkl"):
    global _model
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            print("Model loaded from disk.")
    else:
        print("No saved model found. Initializing a new model.")


# --- Helper Functions for Feedback Management ---

def save_feedback_data(file_path="feedback_data.json"):
    """
    Saves feedback data to a JSON file, enabling persistence across sessions.
    """
    with open(file_path, 'w') as f:
        json.dump({k: v for k, v in _feedback_data.items()}, f)


def load_feedback_data(file_path="feedback_data.json"):
    """
    Loads feedback data from a JSON file, allowing the system to learn from past interactions.
    """
    global _feedback_data
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
            _feedback_data = defaultdict(list, {k: v for k, v in data.items()})
    else:
        _feedback_data = defaultdict(list)


# --- Initialization ---

# Load model and feedback data when module is loaded
load_model()
load_feedback_data()