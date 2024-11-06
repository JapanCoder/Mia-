import time
import threading
from datetime import datetime, timedelta
from typing import Callable, Dict, Any
from task_scheduler import TaskScheduler
from error_logger import ErrorLogger
from feedback_processor import FeedbackProcessor
from self_optimizer import SelfOptimizer
from data_storage import DataStorage

class Scheduler:
    """Handles scheduling, periodic checks, and execution of tasks in the background."""

    def __init__(self, task_scheduler: TaskScheduler, error_logger: ErrorLogger, feedback_processor: FeedbackProcessor, self_optimizer: SelfOptimizer):
        self.task_scheduler = task_scheduler
        self.error_logger = error_logger
        self.feedback_processor = feedback_processor
        self.self_optimizer = self_optimizer
        self.data_storage = DataStorage()
        
        # Dictionary to manage periodic tasks and their intervals
        self.periodic_tasks: Dict[str, Dict[str, Any]] = {}
        self._scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self._scheduler_thread.start()

    def _run_scheduler(self):
        """Continuously checks and executes scheduled tasks."""
        while True:
            try:
                # Check and execute any overdue tasks
                overdue_tasks = self.task_scheduler.check_overdue_tasks()
                for task_name in overdue_tasks:
                    self.execute_task(task_name)
                    
                # Execute periodic tasks based on their defined intervals
                for task_name, task_info in self.periodic_tasks.items():
                    last_run = task_info.get("last_run")
                    interval = task_info.get("interval")
                    if datetime.now() >= last_run + interval:
                        self.execute_task(task_name, periodic=True)
                        self.periodic_tasks[task_name]["last_run"] = datetime.now()
                
                time.sleep(60)  # Wait before checking tasks again
            except Exception as e:
                self.error_logger.log_error("Scheduler Error", e)

    def schedule_task(self, task_name: str, run_time: datetime, details: Dict[str, Any] = None):
        """Schedules a one-time task."""
        return self.task_scheduler.schedule_task(task_name, run_time, details)

    def add_periodic_task(self, task_name: str, interval: timedelta, task_func: Callable, details: Dict[str, Any] = None):
        """
        Adds a task to be run at regular intervals.
        Args:
            task_name (str): Name of the periodic task.
            interval (timedelta): How often to run the task.
            task_func (Callable): The function to call each interval.
            details (dict): Additional task details.
        """
        self.periodic_tasks[task_name] = {
            "task_func": task_func,
            "interval": interval,
            "last_run": datetime.now(),
            "details": details or {}
        }

    def execute_task(self, task_name: str, periodic: bool = False):
        """
        Executes a scheduled or periodic task.
        Args:
            task_name (str): Name of the task to execute.
            periodic (bool): Flag to indicate if the task is periodic.
        """
        try:
            if periodic:
                task_func = self.periodic_tasks[task_name].get("task_func")
                task_func()
            else:
                result = self.task_scheduler.run_task(task_name)
                print(result)

            # Log execution for tracking
            self.log_task_execution(task_name, periodic)

        except Exception as e:
            self.error_logger.log_error(f"Execution Error - {task_name}", e)

    def log_task_execution(self, task_name: str, periodic: bool = False):
        """Logs task execution details."""
        log_data = {
            "task_name": task_name,
            "execution_time": datetime.now().isoformat(),
            "periodic": periodic
        }
        self.data_storage.store_task_log(log_data)

    def start_self_optimization_cycle(self, interval: timedelta):
        """Starts a periodic task to optimize AI behavior based on feedback."""
        self.add_periodic_task(
            "self_optimization",
            interval,
            self.run_self_optimization_cycle
        )

    def run_self_optimization_cycle(self):
        """Runs self-optimization using feedback and past interaction data."""
        try:
            feedback_data = self.feedback_processor.get_all_feedback()
            interaction_data = self.data_storage.retrieve_data("recent_interactions")
            self.self_optimizer.train_from_interactions(interaction_data)
            self.self_optimizer.update_response_patterns(feedback_data)
            print("Self-optimization cycle completed.")
        except Exception as e:
            self.error_logger.log_error("Self-Optimization Error", e)
        
    def cancel_task(self, task_name: str):
        """Cancels a scheduled or periodic task."""
        if task_name in self.periodic_tasks:
            del self.periodic_tasks[task_name]
            print(f"Periodic task '{task_name}' has been canceled.")
        else:
            print(self.task_scheduler.cancel_task(task_name))

    def list_tasks(self) -> Dict[str, Any]:
        """Lists both scheduled and periodic tasks."""
        scheduled_tasks = self.task_scheduler.list_scheduled_tasks()
        periodic_tasks = [
            {
                "task_name": name,
                "interval": task["interval"].total_seconds(),
                "last_run": task["last_run"].isoformat()
            }
            for name, task in self.periodic_tasks.items()
        ]
        return {"scheduled_tasks": scheduled_tasks, "periodic_tasks": periodic_tasks}
    
# Example Usage
if __name__ == "__main__":
    scheduler = Scheduler(TaskScheduler(), ErrorLogger(), FeedbackProcessor(), SelfOptimizer(FeedbackProcessor(), LearningModule()))

    # Schedule a one-time task
    print(scheduler.schedule_task("Backup", datetime.now() + timedelta(minutes=5), {"priority": "high"}))

    # Start a self-optimization cycle every 6 hours
    scheduler.start_self_optimization_cycle(interval=timedelta(hours=6))

    # Add a periodic task
    scheduler.add_periodic_task(
        "data_backup",
        interval=timedelta(hours=1),
        task_func=lambda: print("Running data backup task."),
        details={"priority": "medium"}
    )

    # List all tasks
    print("All tasks:", scheduler.list_tasks())