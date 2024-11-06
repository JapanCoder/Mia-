# command_parser.py

from typing import Dict, Any, Tuple
from nlp_processing import NLPProcessing
from knowledge_manager import KnowledgeManager
from task_scheduler import TaskScheduler
from emotional_analysis import EmotionalAnalysis
from utility_functions import clean_text

# Initialize dependent modules
nlp_processor = NLPProcessing()
knowledge_manager = KnowledgeManager()
task_scheduler = TaskScheduler()
emotional_analysis = EmotionalAnalysis()

class CommandParser:
    def __init__(self):
        # To store context if follow-up commands are expected
        self.context = {}

    # ---- 1. Parse Command ----
    def parse_command(self, text: str) -> Dict[str, Any]:
        """
        Analyzes command intent and returns parsed data.
        Args:
            text (str): User command text.
        Returns:
            Dict[str, Any]: Parsed intent, keywords, and additional info.
        """
        text = clean_text(text)  # Normalize the text
        parsed_data = nlp_processor.parse_intent(text)
        
        # Analyze sentiment to adjust Mia’s responses (optional)
        sentiment = nlp_processor.analyze_sentiment(text)
        parsed_data["sentiment"] = sentiment
        
        # Store the parsed context for potential follow-up
        self.context["last_command"] = parsed_data
        return parsed_data

    # ---- 2. Route Command ----
    def route_to_module(self, parsed_data: Dict[str, Any]) -> Tuple[str, Any]:
        """
        Routes parsed command to appropriate module based on intent.
        Args:
            parsed_data (Dict[str, Any]): Parsed command data.
        Returns:
            Tuple[str, Any]: Result type and processed data.
        """
        intent = parsed_data.get("intent")
        keywords = parsed_data.get("keywords", [])
        
        # Determine routing based on intent
        if intent == "definition":
            return "knowledge", knowledge_manager.retrieve_definition(keywords)
        
        elif intent == "recommendation":
            return "recommendation", knowledge_manager.get_recommendations(keywords)
        
        elif intent == "creation":
            return "task", task_scheduler.create_task(keywords)
        
        else:
            return "fallback", self.fallback_handler(parsed_data)

    # ---- 3. Handle Follow-Up Commands ----
    def handle_follow_up(self, text: str) -> Tuple[str, Any]:
        """
        Interprets and processes follow-up commands based on previous context.
        Args:
            text (str): Follow-up command text.
        Returns:
            Tuple[str, Any]: Result type and processed data.
        """
        last_command = self.context.get("last_command")
        if not last_command:
            return "error", "No prior command context available."

        # Continue based on previous intent
        intent = last_command["intent"]
        return self.route_to_module({"intent": intent, "keywords": [text]})

    # ---- 4. Validate Command ----
    def validate_command(self, parsed_data: Dict[str, Any]) -> bool:
        """
        Ensures that the parsed command has a valid structure.
        Args:
            parsed_data (Dict[str, Any]): Parsed command data.
        Returns:
            bool: True if valid, False otherwise.
        """
        intent = parsed_data.get("intent")
        if not intent or intent == "unknown":
            return False
        return True

    # ---- 5. Fallback Handler ----
    def fallback_handler(self, parsed_data: Dict[str, Any]) -> str:
        """
        Handles unsupported or ambiguous commands.
        Args:
            parsed_data (Dict[str, Any]): Parsed command data.
        Returns:
            str: Fallback response message.
        """
        return "I'm not sure how to handle that command. Can you please rephrase?"

# Test cases for CommandParser
if __name__ == "__main__":
    command_parser = CommandParser()
    
    # Test parsing and routing a command
    text = "Can you recommend a book?"
    parsed_data = command_parser.parse_command(text)
    if command_parser.validate_command(parsed_data):
        result_type, result_data = command_parser.route_to_module(parsed_data)
        print(f"Result Type: {result_type}, Data: {result_data}")
    else:
        print("Invalid command format.")

    # Test handling follow-up command
    follow_up_text = "Specifically a mystery novel."
    follow_up_result_type, follow_up_result_data = command_parser.handle_follow_up(follow_up_text)
    print(f"Follow-Up Result Type: {follow_up_result_type}, Data: {follow_up_result_data}")