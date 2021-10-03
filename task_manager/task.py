from scheduler.scheduler import Scheduler
from threading import Thread, Event


class Task:
    def __init__(self, scheduler: 'Scheduler', task: callable, args: tuple=None, kwargs: dict=None):
        self.scheduler = scheduler
        self._stop_event = Event()
        self._thread = Thread(target=self._task_handler)

        self.task = task
        self.task_args = tuple(args or ())
        self.task_kwargs = dict(kwargs or {})
    
    def __repr__(self):
        return f"Task(scheduler={self.scheduler}, task={self.task}, task_args={self.task_args}, task_kwargs={self.task_kwargs})"
    
    def _task_handler(self) -> None:
        while not self._stop_event.is_set():
            self.scheduler.sleep_until_execution()
            print(f"Executing the task {self.task.__name__}, next execution: {self.scheduler.next_execution}")
            self.task(*self.task_args, **self.task_kwargs)
    
    def is_running(self) -> bool:
        return self._thread.is_running()

    def run(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
