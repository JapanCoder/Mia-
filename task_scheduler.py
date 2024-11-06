from datetime import datetime, timedelta

# Placeholder imports for context management, feedback, and learning modules
import context_manager
import feedback_processor
import learning_module

class TaskScheduler:
    """Manages scheduling, executing, and tracking tasks."""

    def __init__(self):
        self.tasks = {}  # Dictionary to hold tasks with task_name as key and details as value
    
    def schedule_task(self, task_name: str, run_time: datetime, details: dict = None) -> str:
        """
        Schedules a task to run at a specified time.
        """
        self.tasks[task_name] = {
            "run_time": run_time,
            "details": details or {},
            "status": "scheduled"
        }
        return f"Task '{task_name}' scheduled for {run_time.strftime('%Y-%m-%d %H:%M:%S')}."

    def run_task(self, task_name: str) -> str:
        """
        Runs a scheduled task immediately if it exists.
        """
        task = self.tasks.get(task_name)
        if task and task["status"] == "scheduled":
            # Execute the task logic here, e.g., via a method or callback defined in `details`
            task["status"] = "completed"
            return f"Task '{task_name}' executed successfully."
        return f"Task '{task_name}' not found or already completed."

    def check_overdue_tasks(self) -> list:
        """
        Checks for any overdue tasks and returns them.
        """
        current_time = datetime.now()
        overdue_tasks = []
        for name, task in self.tasks.items():
            if task["status"] == "scheduled" and task["run_time"] < current_time:
                overdue_tasks.append(name)
                task["status"] = "overdue"
        return overdue_tasks

    def cancel_task(self, task_name: str) -> str:
        """
        Cancels a scheduled task.
        """
        if task_name in self.tasks:
            del self.tasks[task_name]
            return f"Task '{task_name}' has been canceled."
        return f"Task '{task_name}' not found."

    def list_scheduled_tasks(self) -> list:
        """
        Lists all scheduled tasks with their status.
        """
        return [
            {
                "task_name": name,
                "run_time": task["run_time"].strftime('%Y-%m-%d %H:%M:%S'),
                "status": task["status"],
                "details": task["details"]
            }
            for name, task in self.tasks.items()
        ]

# Example usage
scheduler = TaskScheduler()

# Schedule a task
print(scheduler.schedule_task("Backup Data", datetime.now() + timedelta(hours=1), {"priority": "high"}))

# List scheduled tasks
print("Scheduled tasks:", scheduler.list_scheduled_tasks())

# Check for overdue tasks
print("Overdue tasks:", scheduler.check_overdue_tasks())

# Run a task
print(scheduler.run_task("Backup Data"))

# Cancel a task
print(scheduler.cancel_task("Backup Data"))