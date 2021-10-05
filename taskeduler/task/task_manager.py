from time import sleep
from threading import Thread, Event

from taskeduler.task.task import Task


class TaskAlreadyExists(Exception):
    """This exception is raised when a task name already exists."""
    def __init__(self, task_name: str):
        self.message = f"'{task_name}' already exists, please set override=True if you want to override it."


class LoopManager:
    """
    This class manages the infinite loop that is running to prevent the program to stop.

    Args:
        sleep_interval (int; optional): The time that passes in the infinite loop between stop comprobations.
    """
    def __init__(self, sleep_interval=60):
        self.sleep_interval = sleep_interval

        self._loop = Thread(target=self._exist)
        self._stop_event = Event()
    
    def _exist(self):
        """Run the loop in a thread"""
        while not self._stop_event.is_set():
            sleep(self.sleep_interval)

    def start(self):
        """Start the loop"""
        print("Starting loop...")
        self._loop.start()

    def stop(self):
        """Stop the loop"""
        self._stop_event.set()


class TaskManager:
    """
    This class manages all the executing tasks and the infinite loop.
    """
    def __init__(self) -> None:
        self.loop = LoopManager()
        self.tasks = dict()

    def add_task(self, task_name: str, task: Task, override:bool=False) -> None:
        """Add a new task to be executed."""
        if task_name in self.tasks:
            if override:
                self.remove_task(task_name)
            else:
                raise TaskAlreadyExists(task_name)
        
        self.tasks[task_name] = task
        self.tasks[task_name].run()

    def remove_task(self, task_name: str) -> None:
        """Stop and remove a task that is being executed."""
        self.tasks[task_name].stop()
        self.tasks.pop(task_name)
