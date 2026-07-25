from typing import Dict, List

__version__ = "1.0.0"

class Task:
    """A class representing a task.

    Attributes:
        name (str): The name of the task.
        description (str): The description of the task.
    """
    def __init__(self, name: str, description: str) -> None:
        """Initialize a Task object.

        Args:
            name (str): The name of the task.
            description (str): The description of the task.
        """
        self.name = name
        self.description = description

    def execute(self) -> None:
        """Execute the task.

        Returns:
            None
        """
        print(f"Executing task: {self.name}")

    def get_status(self) -> str:
        """Get the status of the task.

        Returns:
            str: The status of the task.
        """
        return "Completed"

def task1() -> None:
    """A function representing a task.

    Returns:
        None
    """
    print("Task 1 executed")

def task2(name: str, description: str) -> None:
    """A function representing a task.

    Args:
        name (str): The name of the task.
        description (str): The description of the task.
    Returns:
        None
    """
    print(f"Task {name} executed: {description}")
