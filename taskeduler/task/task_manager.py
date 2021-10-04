from taskeduler.task.task import Task

from threading import Thread, Event
from time import sleep


class TaskAlreadyExists(Exception):
    def __init__(self, task_name: str):
        self.message = f"'{task_name}' already exists, please set override=True if you want to override it."


class LoopManager:
    def __init__(self, sleep_interval=60):
        self.sleep_interval = sleep_interval

        self._loop = Thread(target=self._exist)
        self._stop_event = Event()
    
    def _exist(self):
        while not self._stop_event.is_set():
            sleep(self.sleep_interval)

    def start(self):
        print("Starting loop...")
        self._loop.start()

    def stop(self):
        self._stop_event.set()


class TaskManager:
    def __init__(self) -> None:
        self.loop = LoopManager()
        self.tasks = dict()

    def add_task(self, task_name: str, task: Task, override:bool=False) -> None:
        if task_name in self.tasks:
            if override:
                self.remove_task(task_name)
            else:
                raise TaskAlreadyExists(task_name)
        
        self.tasks[task_name] = task
        self.tasks[task_name].run()

    def remove_task(self, task_name: str) -> None:
        self.tasks[task_name].stop()
        self.tasks.pop(task_name)
