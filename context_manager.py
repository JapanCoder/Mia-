import datetime
import time
import json
import os

class ContextManager:
    CONTEXT_PRIORITY = ["activity", "time_of_day", "preferences", "temporary_state"]

    def __init__(self, context_file="context.json"):
        self.context_file = context_file
        self.context_data = {
            "activity": None,
            "time_of_day": None,
            "recent_interactions": [],
            "preferences": {},
            "temporary_state": {}
        }
        self.load_context()

    # --- Core Context Functions ---
    def get_context(self, user_input=None):
        """
        Retrieves the prioritized context with dynamic data updates.
        Advanced handling of temporary states and recent interactions.
        
        Parameters:
        - user_input: str, input text from user, if available.
        
        Returns:
        - dict, the context relevant to the conversation.
        """
        self.context_data["time_of_day"] = self.get_time_of_day()
        self.infer_activity_from_interactions()

        # Build context with only prioritized fields that are non-null
        context = {
            key: value
            for key, value in self.context_data.items()
            if key in self.CONTEXT_PRIORITY and value is not None
        }
        context["temporary_state"] = {
            k: v for k, v in self.context_data["temporary_state"].items()
            if v["expiry"] > time.time()
        }

        # If there's no active context, assume a default state
        if not any(context.values()):
            context["status"] = "no_active_context"

        if user_input:
            self.update_recent_interactions(user_input)

        return context

    def update_context(self, key, value):
        """
        Updates context data with error handling and conditional insertion.
        Supports handling nested dictionaries for specific keys.
        """
        if key == "recent_interactions":
            if isinstance(value, dict) and len(self.context_data[key]) < 10:  # Limit stored interactions
                self.context_data[key].append(value)
        elif key in self.context_data:
            if isinstance(self.context_data[key], dict) and isinstance(value, dict):
                self.context_data[key].update(value)
            else:
                self.context_data[key] = value

    def clear_context(self):
        """
        Resets specific context fields to defaults, preserving certain user preferences.
        Only removes expired temporary states.
        """
        self.context_data.update({
            "activity": None,
            "time_of_day": self.get_time_of_day(),
            "recent_interactions": []
        })
        # Remove only expired states from temporary_state
        self.context_data["temporary_state"] = {
            k: v for k, v in self.context_data["temporary_state"].items()
            if v["expiry"] > time.time()
        }

    # --- Helper Functions ---
    def get_time_of_day(self):
        """
        Determines time of day with advanced conditional logic based on hour intervals.
        """
        hour = datetime.datetime.now().hour
        return (
            "morning" if 5 <= hour < 12
            else "afternoon" if 12 <= hour < 17
            else "evening" if 17 <= hour < 21
            else "night"
        )

    def save_context(self):
        """
        Saves the current context to a file with error handling.
        If save fails, logs error for review without terminating program.
        """
        try:
            with open(self.context_file, 'w') as f:
                json.dump(self.context_data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Error saving context: {e}")

    def load_context(self):
        """
        Loads context from a file if it exists, else initializes time of day.
        """
        try:
            if os.path.exists(self.context_file):
                with open(self.context_file, 'r') as f:
                    self.context_data = json.load(f)
            else:
                self.context_data["time_of_day"] = self.get_time_of_day()
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading context: {e}")
            self.context_data["time_of_day"] = self.get_time_of_day()

    # --- Additional Context Management Functions ---
    def infer_activity_from_interactions(self):
        """
        Analyzes recent interactions to infer current activity with complex pattern matching.
        """
        recent_texts = " ".join(self.get_recent_interactions())
        activity = (
            "work" if any(keyword in recent_texts for keyword in ["meeting", "email"])
            else "leisure" if any(keyword in recent_texts for keyword in ["relax", "movie"])
            else None
        )
        self.context_data["activity"] = activity

    def set_temporary_state(self, key, value, duration=1800):
        """
        Sets a temporary state with expiry.
        If a temporary state already exists for the key, extends the duration.
        """
        if key in self.context_data["temporary_state"]:
            self.context_data["temporary_state"][key]["expiry"] += duration
        else:
            self.context_data["temporary_state"][key] = {"value": value, "expiry": time.time() + duration}

    def get_temporary_state(self, key):
        """
        Retrieves a temporary state if it’s still active, removes it if expired.
        """
        state = self.context_data["temporary_state"].get(key)
        if state:
            if state["expiry"] > time.time():
                return state["value"]
            del self.context_data["temporary_state"][key]
        return None

    def handle_event(self, event):
        """
        Processes specific events (e.g., login/logout) by adjusting context.
        Login resets activity, logout saves current context.
        """
        event_handlers = {
            "login": lambda: (self.update_context("activity", "starting_day"), self.clear_context()),
            "logout": self.save_context
        }
        handler = event_handlers.get(event)
        if handler:
            handler()

    def get_recent_interactions(self, limit=5):
        """
        Retrieves a limited set of recent interactions for context inference.
        """
        return [interaction for interaction in self.context_data["recent_interactions"][-limit:]]

    def add_preference(self, key, value):
        """
        Adds or updates a user preference.
        """
        self.context_data["preferences"][key] = value

    def get_preferences(self):
        """
        Returns current preferences in the context data.
        """
        return self.context_data["preferences"]

    def update_recent_interactions(self, user_input):
        """
        Adds the latest user input to recent interactions for contextual analysis.
        
        Parameters:
        - user_input: str, the text input from the user.
        """
        self.update_context("recent_interactions", user_input)