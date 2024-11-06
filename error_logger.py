import logging
from datetime import datetime

class ErrorLogger:
    def __init__(self, log_file: str = "error_log.txt", log_level: int = logging.ERROR):
        """
        Initializes the error logger with a specified log file and log level.
        Args:
            log_file (str): The file where error logs will be saved.
            log_level (int): The logging level, e.g., ERROR, WARNING, INFO.
        """
        # Set up the logging configuration
        self.logger = logging.getLogger("MiaErrorLogger")
        self.logger.setLevel(log_level)

        # Create a file handler to write logs to a file
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)

        # Create a console handler to optionally output errors to the console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)  # Set to WARNING to avoid excessive console logging

        # Set a logging format
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log_error(self, message: str, exception: Exception = None):
        """
        Logs an error message with an optional exception.
        Args:
            message (str): The error message to log.
            exception (Exception, optional): An optional exception instance to include.
        """
        if exception:
            message = f"{message} | Exception: {exception}"
        self.logger.error(message)

    def log_warning(self, message: str):
        """
        Logs a warning message.
        Args:
            message (str): The warning message to log.
        """
        self.logger.warning(message)

    def log_info(self, message: str):
        """
        Logs an informational message.
        Args:
            message (str): The informational message to log.
        """
        self.logger.info(message)

    def log_critical(self, message: str):
        """
        Logs a critical error message that may indicate system failure.
        Args:
            message (str): The critical error message to log.
        """
        self.logger.critical(message)

    def get_recent_logs(self, count: int = 10) -> list:
        """
        Retrieves the most recent log entries from the log file.
        Args:
            count (int): The number of recent logs to retrieve.
        Returns:
            list: A list of recent log entries as strings.
        """
        try:
            with open("error_log.txt", "r") as file:
                logs = file.readlines()
            # Get the most recent 'count' logs
            return logs[-count:]
        except FileNotFoundError:
            self.log_error("Log file not found.")
            return []

# Example usage
if __name__ == "__main__":
    logger = ErrorLogger()

    # Log different levels of messages
    logger.log_info("System started successfully.")
    logger.log_warning("This is a warning message.")
    logger.log_error("An error occurred while processing the request.")
    logger.log_critical("Critical system failure encountered.")
    
    # Retrieve and print recent logs
    recent_logs = logger.get_recent_logs(5)
    print("Recent logs:")
    for log in recent_logs:
        print(log.strip())