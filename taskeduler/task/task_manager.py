from os import X_OK
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
    def __init__(self, loop_function=None, sleep_interval=60):
        self.sleep_interval = sleep_interval
        if loop_function is None:
            loop_function = lambda: sleep(self.sleep_interval)
        
        self.loop_function = loop_function
        self._stop_event = Event()

        self._loop = Thread(target=self._exist, args=(self._stop_event, self.loop_function))
        self._running = False
    
    def _exist(self, stop_event, loop_function):
        """Run the loop in a thread"""
        while not stop_event.is_set():
            loop_function()

    def start(self, in_thread=True):
        """Start the loop"""
        if self._running:
            print("Loop already running.")
        elif not in_thread:
            print("Starting loop...")
            self._running = True
            self._exist(self._stop_event, self.loop_function)
        elif self._running is not None:
            print("Starting loop...")
            self._loop.start()
            self._running = True
        else:
            print("The loop was stopped and cannot be runed again in thread mode.")


    def stop(self):
        """Stop the loop"""
        if self._running:
            print("Stopping loop...")
            self._stop_event.set()
            self._running = None
        else:
            print("Loop already stopped.")
    
    def is_running(self):
        return bool(self._running)


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
