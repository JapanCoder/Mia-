from datetime import datetime
from utility_functions import save_to_json, load_from_json, format_datetime
from context_manager import ContextManager
from learning_module import fetch_dynamic_response, save_response, adapt_response_patterns
from feedback_processor import process_feedback
from emotional_analysis import EmotionalAnalysis

# Initialize EmotionalAnalysis and ContextManager
emotional_analysis = EmotionalAnalysis()
context_manager = ContextManager()  # Instantiate ContextManager

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
    Starts a new session, setting the start time and initializing interaction and feedback storage.
    """
    global _current_session
    _current_session.update({
        "start_time": datetime.now().isoformat(),
        "interactions": [],
        "feedback": []
    })
    print(f"Session started at {_current_session['start_time']}")


def end_session():
    """
    Ends the current session by setting the end time and saving session data to persistent storage.
    """
    global _current_session
    _current_session["end_time"] = datetime.now().isoformat()
    save_session_data(_current_session)
    print(f"Session ended at {_current_session['end_time']}")


def save_session_data(session_data, file_path=None):
    """
    Saves the given session data to a JSON file. If the file already contains session data, appends to it.
    """
    file_path = file_path or SESSION_DATA_PATH
    try:
        all_sessions = load_from_json(file_path) or []
    except (IOError, ValueError) as e:
        print(f"Error loading sessions: {e}")
        all_sessions = []
    
    # Ensure all_sessions is a list, even if the file contains unexpected data
    if not isinstance(all_sessions, list):
        all_sessions = [all_sessions]
    
    all_sessions.append(session_data)
    
    try:
        save_to_json(all_sessions, file_path)
    except IOError as e:
        print(f"Error saving session data: {e}")


# --- Interaction Tracking Functions ---

def log_interaction(user_input, response, emotion=None):
    """
    Logs a single interaction, capturing the user input, system response, and emotion if provided.
    """
    interaction = {
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "response": response,
        "emotion": emotion,
        "context": context_manager.get_context()  # Use ContextManager instance to get context
    }
    _current_session["interactions"].append(interaction)
    print(f"Logged interaction: {interaction}")


def get_recent_interactions(n=5):
    """
    Retrieves the most recent interactions, up to the number specified.
    """
    return _current_session["interactions"][-n:]


# --- Feedback Management Functions ---

def add_feedback(feedback_entry):
    """
    Adds feedback to the current session, processes it, and adapts response patterns.
    """
    _current_session["feedback"].append(feedback_entry)
    process_feedback(feedback_entry)
    adapt_response_patterns()


def get_cumulative_feedback():
    """
    Computes the average rating and feedback count from the current session's feedback.
    """
    if not _current_session["feedback"]:
        return {"average_rating": 0.0, "count": 0}
    
    ratings = [f.get('rating') for f in _current_session["feedback"] if 'rating' in f]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0.0
    return {"average_rating": avg_rating, "count": len(ratings)}


# --- Learning and Context Integration ---

def get_dynamic_response(user_input):
    """
    Retrieves a dynamic response based on the user input, analyzing emotion and integrating context.
    """
    context = context_manager.get_context()  # Use ContextManager instance to get context
    emotion_state = emotional_analysis.analyze_emotion(user_input)
    response = fetch_dynamic_response(user_input, context)
    
    # Log interaction with the derived emotion and context
    log_interaction(user_input, response, emotion=emotion_state.emotion if emotion_state else None)
    return response


def continue_from_previous_session():
    """
    Attempts to continue from the last session by loading the context of the previous session.
    """
    try:
        all_sessions = load_from_json(SESSION_DATA_PATH) or []
    except (IOError, ValueError) as e:
        print(f"Error loading previous sessions: {e}")
        return
    
    if all_sessions:
        last_session = all_sessions[-1]
        if "context" in last_session:
            context_manager.update_context("context", last_session["context"])  # Update using ContextManager instance
            print(f"Continuing from previous session with context: {last_session['context']}")