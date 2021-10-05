from threading import Thread, Event

from taskeduler.scheduler import Scheduler


class Task:
    """
    This class represents a task that will be executed.

    Args:
        scheduler (Scheduler): The scheduler object that will mark the execution patterns.
        task (callable): The entrypoint function that is going to be executed.
        args (tuple; optional): The arguments to be passed to the ``task`` entrypoint.
        kwargs (dict; optional): The keyword arguments to be passed to the ``task`` entrypoint.
    """
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
        """
        This method is the real thing that is being executed in the task Thread.
        It waits until it can be executed and then it is executed, repeating this cycle until the task is told to stop.
        """
        while not self._stop_event.is_set():
            self.scheduler.sleep_until_execution()
            print(f"Executing the task {self.task.__name__}, next execution: {self.scheduler.next_execution}")
            self.task(*self.task_args, **self.task_kwargs)
    
    def is_running(self) -> bool:
        """Returns if the task is currently running."""
        return self._thread.is_running()

    def run(self) -> None:
        """Starts the task."""
        self._thread.start()

    def stop(self) -> None:
        """Stops the task."""
        self._stop_event.set()
