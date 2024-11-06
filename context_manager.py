import datetime
import time
import json
import os

# Dictionary to hold the context data
_context_data = {
    "activity": None,
    "time_of_day": None,
    "recent_interactions": [],
    "preferences": {},
    "temporary_state": {}
}

CONTEXT_PRIORITY = ["activity", "time_of_day", "preferences", "temporary_state"]

# --- Helper Functions ---

def get_time_of_day():
    """
    Helper function to determine the time of day based on the current hour.
    
    Returns:
    - str: Time of day ('morning', 'afternoon', 'evening', or 'night').
    """
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    else:
        return "night"


def save_context(file_path="context.json"):
    """
    Saves the current context to a JSON file for session persistence.
    """
    with open(file_path, 'w') as f:
        json.dump(_context_data, f)


def load_context(file_path="context.json"):
    """
    Loads the context from a JSON file, if it exists, for session continuity.
    """
    global _context_data
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            _context_data = json.load(f)
    else:
        # Initialize with time_of_day in case no context file exists
        _context_data["time_of_day"] = get_time_of_day()


# --- Core Context Functions ---

def get_context():
    """
    Retrieves the current context data.
    
    Returns:
    - dict: Current context information including prioritized items.
    """
    _context_data["time_of_day"] = get_time_of_day()  # Update dynamically
    infer_activity_from_interactions()  # Infer activity based on recent interactions
    return {k: _context_data[k] for k in CONTEXT_PRIORITY if _context_data[k] is not None}


def update_context(key, value):
    """
    Updates a specific context attribute with a new value.
    
    Args:
    - key (str): The context key to update (e.g., 'activity', 'preferences').
    - value (Any): The new value to assign to the context key.
    """
    if key == "recent_interactions":
        _context_data[key].append(value)
    else:
        _context_data[key] = value


def clear_context():
    """
    Clears all non-persistent context data.
    """
    _context_data["activity"] = None
    _context_data["temporary_state"] = {}
    _context_data["recent_interactions"] = []


# --- Additional Context Management Functions ---

def infer_activity_from_interactions():
    """
    Infers the activity based on recent interactions, updating the activity context dynamically.
    """
    recent_texts = " ".join(get_recent_interactions())
    if "meeting" in recent_texts or "email" in recent_texts:
        _context_data["activity"] = "work"
    elif "relax" in recent_texts or "movie" in recent_texts:
        _context_data["activity"] = "leisure"


def set_temporary_state(key, value, duration=1800):
    """
    Sets a temporary state with an expiry duration.
    
    Args:
    - key (str): The temporary state key.
    - value (Any): The value of the temporary state.
    - duration (int): Duration in seconds for which the state remains valid.
    """
    _context_data["temporary_state"][key] = {"value": value, "expiry": time.time() + duration}


def get_temporary_state(key):
    """
    Retrieves a temporary state if it hasn't expired; otherwise, clears it.
    
    Args:
    - key (str): The temporary state key to retrieve.
    
    Returns:
    - Any: The value of the temporary state if valid, else None.
    """
    state = _context_data["temporary_state"].get(key)
    if state and state["expiry"] > time.time():
        return state["value"]
    elif state:
        del _context_data["temporary_state"][key]  # Clean up expired states
    return None


def handle_event(event):
    """
    Responds to specific events by updating or clearing relevant context.
    
    Args:
    - event (str): The event type (e.g., 'login', 'logout').
    """
    if event == "login":
        update_context("activity", "starting_day")
        clear_context()
    elif event == "logout":
        save_context()


def get_recent_interactions(limit=5):
    """
    Retrieves recent interactions with a specified limit.
    
    Args:
    - limit (int): Number of recent interactions to retrieve (default is 5).
    
    Returns:
    - list: Recent interactions, up to the specified limit.
    """
    return _context_data["recent_interactions"][-limit:]


def add_preference(key, value):
    """
    Adds or updates a user preference.
    
    Args:
    - key (str): The preference key (e.g., 'theme', 'language').
    - value (Any): The preference value.
    """
    _context_data["preferences"][key] = value


def get_preferences():
    """
    Retrieves the stored user preferences.
    
    Returns:
    - dict: Dictionary of user preferences.
    """
    return _context_data["preferences"]