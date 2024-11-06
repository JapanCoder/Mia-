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
    def get_context(self):
        self.context_data["time_of_day"] = self.get_time_of_day()  # Update dynamically
        self.infer_activity_from_interactions()
        return {k: self.context_data[k] for k in self.CONTEXT_PRIORITY if self.context_data[k] is not None}

    def update_context(self, key, value):
        if key == "recent_interactions":
            self.context_data[key].append(value)
        else:
            self.context_data[key] = value

    def clear_context(self):
        self.context_data["activity"] = None
        self.context_data["temporary_state"] = {}
        self.context_data["recent_interactions"] = []

    # --- Helper Functions ---
    def get_time_of_day(self):
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 21:
            return "evening"
        else:
            return "night"

    def save_context(self):
        with open(self.context_file, 'w') as f:
            json.dump(self.context_data, f)

    def load_context(self):
        if os.path.exists(self.context_file):
            with open(self.context_file, 'r') as f:
                self.context_data = json.load(f)
        else:
            self.context_data["time_of_day"] = self.get_time_of_day()

    # --- Additional Context Management Functions ---
    def infer_activity_from_interactions(self):
        recent_texts = " ".join(self.get_recent_interactions())
        if "meeting" in recent_texts or "email" in recent_texts:
            self.context_data["activity"] = "work"
        elif "relax" in recent_texts or "movie" in recent_texts:
            self.context_data["activity"] = "leisure"

    def set_temporary_state(self, key, value, duration=1800):
        self.context_data["temporary_state"][key] = {"value": value, "expiry": time.time() + duration}

    def get_temporary_state(self, key):
        state = self.context_data["temporary_state"].get(key)
        if state and state["expiry"] > time.time():
            return state["value"]
        elif state:
            del self.context_data["temporary_state"][key]
        return None

    def handle_event(self, event):
        if event == "login":
            self.update_context("activity", "starting_day")
            self.clear_context()
        elif event == "logout":
            self.save_context()

    def get_recent_interactions(self, limit=5):
        return self.context_data["recent_interactions"][-limit:]

    def add_preference(self, key, value):
        self.context_data["preferences"][key] = value

    def get_preferences(self):
        return self.context_data["preferences"]

# Example usage
context_manager = ContextManager()