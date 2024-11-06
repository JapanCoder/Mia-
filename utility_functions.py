from datetime import datetime, timedelta
import re
import json
import os


# --- Date and Time Utilities ---

def format_datetime(dt, fmt="%A, %I:%M %p"):
    """
    Converts a datetime object into a user-friendly string format.

    Args:
    - dt (datetime): The datetime object to format.
    - fmt (str): The format string for the datetime.

    Returns:
    - str: Formatted date and time string.
    """
    return dt.strftime(fmt)


def time_until(future_time):
    """
    Calculates the time remaining until a specific datetime.

    Args:
    - future_time (datetime): The future datetime to count down to.

    Returns:
    - timedelta: Time remaining until the future time.
    """
    return future_time - datetime.now()


# --- String Utilities ---

def clean_text(text):
    """
    Cleans a string by removing special characters and extra whitespace.

    Args:
    - text (str): The text to clean.

    Returns:
    - str: Cleaned text.
    """
    return re.sub(r'\s+', ' ', re.sub(r'[^A-Za-z0-9 ]+', '', text)).strip()


def truncate_text(text, length=100):
    """
    Truncates text to a specified length with ellipsis if necessary.

    Args:
    - text (str): The text to truncate.
    - length (int): Maximum length of the text.

    Returns:
    - str: Truncated text with ellipsis.
    """
    return text if len(text) <= length else text[:length] + "..."


# --- Feedback Utilities ---

def average_feedback_score(feedback_list):
    """
    Calculates the average feedback score from a list of feedback entries.

    Args:
    - feedback_list (list of dict): List of feedback entries, each with a 'rating' key.

    Returns:
    - float: Average feedback score.
    """
    scores = [f.get('rating', 0) for f in feedback_list if 'rating' in f]
    return sum(scores) / len(scores) if scores else 0.0


# --- JSON File Management Utilities ---

def save_to_json(data, file_path):
    """
    Saves data to a JSON file.

    Args:
    - data (dict or list): Data to save.
    - file_path (str): Path to the JSON file.
    """
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def load_from_json(file_path):
    """
    Loads data from a JSON file.

    Args:
    - file_path (str): Path to the JSON file.

    Returns:
    - dict or list: Loaded data.
    """
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return {}


# --- Context Utilities ---

def is_during_work_hours(start_hour=9, end_hour=17):
    """
    Checks if the current time is within work hours.

    Args:
    - start_hour (int): Start of work hours (24-hour format).
    - end_hour (int): End of work hours (24-hour format).

    Returns:
    - bool: True if current time is within work hours, else False.
    """
    current_hour = datetime.now().hour
    return start_hour <= current_hour < end_hour