from datetime import datetime
from utility_functions import save_to_json, load_from_json, format_datetime
from context_manager import get_context, update_context
from learning_module import fetch_dynamic_response, save_response, adapt_response_patterns
from feedback_module import process_feedback
from emotional_analysis import detect_emotion  # Importing from the emotion module

# Path for saving session data
SESSION_DATA_PATH = "session_data.json"

# In-memory session storage for ongoing session
_current_session = {
    "start_time": None,
    "end_time": None,
    "interactions": [],
    "feedback": []
}

# --- Session Management Functions ---

def start_session():
    """
    Initializes a new session, setting the start time and resetting interactions and feedback.
    """
    global _current_session
    _current_session["start_time"] = datetime.now()
    _current_session["interactions"] = []
    _current_session["feedback"] = []
    print(f"Session started at {format_datetime(_current_session['start_time'])}")


def end_session():
    """
    Ends the current session by setting the end time and saving session data to disk.
    """
    global _current_session
    _current_session["end_time"] = datetime.now()
    save_session_data(_current_session)
    print(f"Session ended at {format_datetime(_current_session['end_time'])}")


def save_session_data(session_data, file_path=SESSION_DATA_PATH):
    """
    Saves session data to a JSON file for later retrieval.

    Args:
    - session_data (dict): The session data to save.
    - file_path (str): Path to the JSON file.
    """
    all_sessions = load_from_json(file_path)
    if isinstance(all_sessions, list):
        all_sessions.append(session_data)
    else:
        all_sessions = [session_data]
    save_to_json(all_sessions, file_path)


# --- Interaction Tracking Functions ---

def log_interaction(user_input, response, emotion=None):
    """
    Logs each interaction within the current session.

    Args:
    - user_input (str): The user's input message.
    - response (str): The response provided.
    - emotion (str): Detected emotion (if available).
    """
    interaction = {
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "response": response,
        "emotion": emotion,
        "context": get_context()
    }
    _current_session["interactions"].append(interaction)
    print(f"Logged interaction: {interaction}")


def get_recent_interactions(n=5):
    """
    Retrieves the last N interactions within the session for contextual continuity.

    Args:
    - n (int): The number of recent interactions to retrieve.

    Returns:
    - list of dict: Recent interactions.
    """
    return _current_session["interactions"][-n:]


# --- Feedback Management Functions ---

def add_feedback(feedback_entry):
    """
    Adds user feedback to the current session and updates feedback in learning and feedback modules.

    Args:
    - feedback_entry (dict): Feedback data (e.g., rating, comment).
    """
    _current_session["feedback"].append(feedback_entry)
    process_feedback(feedback_entry)  # Update feedback module
    adapt_response_patterns()  # Adjust response patterns based on feedback


def get_cumulative_feedback():
    """
    Calculates cumulative feedback for the session for long-term interaction analysis.

    Returns:
    - dict: Summary of feedback (e.g., average rating).
    """
    if not _current_session["feedback"]:
        return {"average_rating": 0.0, "count": 0}
    
    ratings = [f.get('rating', 0) for f in _current_session["feedback"]]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0.0
    return {"average_rating": avg_rating, "count": len(ratings)}


# --- Learning and Context Integration ---

def get_dynamic_response(user_input):
    """
    Fetches a response dynamically based on current context and session data.

    Args:
    - user_input (str): User's input to shape the response.

    Returns:
    - str: Generated response.
    """
    context = get_context()
    emotion = detect_emotion(user_input)  # Using detect_emotion from the emotion module
    response = fetch_dynamic_response(emotion, intensity=1, context=context.get('activity', 'general'))
    log_interaction(user_input, response, emotion)
    return response


def continue_from_previous_session():
    """
    Loads context from the most recent session to maintain continuity.
    """
    all_sessions = load_from_json(SESSION_DATA_PATH)
    if all_sessions:
        last_session = all_sessions[-1]
        if last_session.get("context"):
            update_context(last_session["context"])  # Restore previous context if available
            print(f"Continuing from previous session with context: {last_session['context']}")