from typing import Dict, Any
from datetime import datetime
from command_parser import CommandParser
from conversation_manager import ConversationManager
from emotional_analysis import EmotionalAnalysis
from task_scheduler import TaskScheduler
from knowledge_manager import KnowledgeManager
from self_optimizer import SelfOptimizer
from security_manager import SecurityManager
from api_connector import APIConnector
from voice_interface import VoiceInterface
from feedback_processor import FeedbackProcessor
from learning_module import LearningModule
from error_logger import ErrorLogger
from data_storage import DataStorage

class CoreLogic:
    def __init__(self):
        # Initialize modules and dependencies
        self.command_parser = CommandParser()
        self.conversation_manager = ConversationManager()
        self.emotional_analysis = EmotionalAnalysis()
        self.task_scheduler = TaskScheduler()
        self.knowledge_manager = KnowledgeManager()
        self.self_optimizer = SelfOptimizer(FeedbackProcessor(), LearningModule())
        self.security_manager = SecurityManager()
        self.api_connector = APIConnector()
        self.voice_interface = VoiceInterface()
        self.error_logger = ErrorLogger()
        self.data_storage = DataStorage()
        self.context = {}  # Store interaction context for ongoing sessions

    def process_input(self, user_input: str) -> str:
        """
        Primary handler for user input.
        - Validates user security.
        - Parses command, routes it to the correct module, and logs errors if any occur.
        """
        if not self.security_manager.verify_user(user_input):
            return "User verification failed. Please authenticate."

        try:
            parsed_command = self.command_parser.parse_command(user_input)
            
            # Log each command and context for tracking
            self.context['last_command'] = parsed_command
            self.data_storage.save_session_data("last_command", parsed_command)

            if not self.command_parser.validate_command(parsed_command):
                return "I didn't understand that command. Could you please rephrase?"

            response = self.route_command(parsed_command)
            self.log_interaction(user_input, response)  # Log each interaction
            return response

        except Exception as e:
            self.error_logger.log_error("Error processing input", e)
            return "An error occurred while processing your request."

    def route_command(self, parsed_command: Dict[str, Any]) -> str:
        """
        Routes parsed commands to appropriate modules and adjusts based on sentiment, priority, and urgency.
        """
        intent = parsed_command.get("intent")
        context = parsed_command.get("context", {})
        
        if intent == "information":
            return self.handle_information_request(parsed_command)
        elif intent == "task_management":
            return self.handle_task_management(parsed_command)
        elif intent == "emotional_response":
            return self.handle_emotional_response(parsed_command)
        elif intent == "external_api":
            return self.handle_external_api(parsed_command)
        elif intent == "voice_command":
            return self.handle_voice_command(parsed_command)
        elif intent == "self_optimization":
            return self.initiate_self_optimization(context)
        else:
            return self.conversation_manager.fallback_response()

    def handle_information_request(self, parsed_command: Dict[str, Any]) -> str:
        """Handles requests for information retrieval, taking context and sentiment into account."""
        keywords = parsed_command.get("keywords", [])
        sentiment = parsed_command.get("sentiment", "neutral")
        
        info = self.knowledge_manager.retrieve_information(keywords)
        # Adjust response based on sentiment analysis
        return self.adjust_response_to_sentiment(info, sentiment)

    def handle_task_management(self, parsed_command: Dict[str, Any]) -> str:
        """Handles task scheduling, execution, and cancellation."""
        action = parsed_command.get("action")
        task_name = parsed_command.get("task_name")
        run_time = parsed_command.get("run_time")
        priority = parsed_command.get("priority", "normal")

        if action == "schedule":
            return self.task_scheduler.schedule_task(task_name, run_time, {"priority": priority})
        elif action == "run":
            return self.task_scheduler.run_task(task_name)
        elif action == "cancel":
            return self.task_scheduler.cancel_task(task_name)
        elif action == "list":
            tasks = self.task_scheduler.list_scheduled_tasks()
            return f"Scheduled Tasks: {tasks}"
        else:
            return "Invalid task action specified."

    def handle_emotional_response(self, parsed_command: Dict[str, Any]) -> str:
        """Generates responses based on emotional sentiment analysis."""
        sentiment = parsed_command.get("sentiment", "neutral")
        mood_adjustment = self.emotional_analysis.analyze_emotion(sentiment)
        
        response = self.conversation_manager.generate_response(mood_adjustment)
        return response

    def handle_external_api(self, parsed_command: Dict[str, Any]) -> str:
        """Processes API-related commands and error handling."""
        api_name = parsed_command.get("api_name")
        params = parsed_command.get("parameters", {})
        
        try:
            response = self.api_connector.fetch_data(api_name, params)
            return f"Data from {api_name}: {response}"
        except Exception as e:
            self.error_logger.log_error(f"API Error - {api_name}", e)
            return "An error occurred while fetching the requested data."

    def handle_voice_command(self, parsed_command: Dict[str, Any]) -> str:
        """Executes commands related to voice interaction, including error handling."""
        action = parsed_command.get("action")
        
        if action == "start_voice":
            return self.voice_interface.start_listening()
        elif action == "stop_voice":
            return self.voice_interface.stop_listening()
        else:
            return "Voice command not recognized."

    def initiate_self_optimization(self, context: Dict[str, Any]) -> str:
        """Triggers Mia's self-optimization routine based on recent interactions and feedback."""
        feedback = context.get("feedback")
        interaction_data = self.data_storage.retrieve_data("recent_interactions")

        if feedback:
            self.self_optimizer.analyze_feedback_trends()
            self.self_optimizer.update_response_patterns({"common_issues": feedback})

        self.self_optimizer.train_from_interactions(interaction_data)
        return "Self-optimization initiated based on recent feedback and interactions."

    def feedback_loop(self, user_feedback: str) -> None:
        """
        Processes user feedback to improve performance and interaction quality.
        """
        feedback_data = {"feedback": user_feedback}
        self.data_storage.save_feedback(feedback_data)

        self.self_optimizer.analyze_feedback_trends()
        self.self_optimizer.update_response_patterns(feedback_data)

    def adjust_response_to_sentiment(self, response: str, sentiment: str) -> str:
        """Modifies response tone based on sentiment analysis."""
        if sentiment == "negative":
            return f"I’m here to help. {response}"
        elif sentiment == "positive":
            return f"That's great to hear! {response}"
        return response

    def log_interaction(self, user_input: str, response: str) -> None:
        """Logs user interactions for feedback analysis."""
        interaction_data = {
            "timestamp": datetime.now().isoformat(),
            "input": user_input,
            "response": response
        }
        self.data_storage.store_interaction(interaction_data)