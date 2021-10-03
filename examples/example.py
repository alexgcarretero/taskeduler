from scheduler.execution_rules_manager import ExecutionRulesManager
from scheduler.scheduler import Scheduler
from task_manager.task import Task
from task_manager.task_manager import TaskManager


def daily_greeting():
    """
    In this example we create a function that greets every day at 10 am, skipping the weekends.
    """
    def greet(name: str) -> None:
        """This is the function that is going to be executed."""
        print(f"Hello {name}... Nice to see you again!")

    # execute the task every day, avoiding the weekends
    scheduler = Scheduler(
        frequency="daily",
        execution_rules_manager=ExecutionRulesManager(
            week_days=["mon", "tue", "wed", "thu", "fri"],
            time=["10:00"]
        )
    )

    print(f"The next execution of the scheduler will be on {scheduler.next_execution}")

    # create the task
    task = Task(scheduler=scheduler, task=greet, args=("Peter",))

    # setup the task_manager
    task_manager = TaskManager()
    task_manager.add_task("daily_greeting", task)

    task_manager.loop.start()


if __name__ == "__main__":
    daily_greeting()
