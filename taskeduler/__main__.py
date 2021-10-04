import os
import traceback
from sys import argv

from taskeduler.task import TaskManager
from taskeduler.parser import TaskParser

USAGE = "python3 -m scheduler yaml_file"


class UsageError(Exception):
    def __init__(self, extra_message: str=""):
        if extra_message:
            extra_message = f"\n{extra_message}"
        super().__init__(f"USAGE: {USAGE}{extra_message}")


def main(task_manager):
    try:
        # Parse yaml
        yaml_file = argv[1]
        if not os.path.exists(yaml_file):
            raise UsageError(f"The file '{yaml_file}' does not exist.")
        task_parser = TaskParser(yaml_file)
        
        # Create TaskManager and add all tasks
        
        for task_name, task in task_parser.tasks.items():
            task_manager.add_task(task_name, task)
        task_manager.loop.start()
    except IndexError:
        raise UsageError()


if __name__ == "__main__":
    task_manager = TaskManager()
    try:
        main(task_manager)
    except UsageError as e:
        print(e)
        exit(-1)
    except Exception:
        traceback.print_exc()
        exit(1)
    except KeyboardInterrupt:
        print("Stopping all the threads and tasks...")
        print(f"This may take up to {task_manager.loop.sleep_interval} seconds...")
        task_manager.loop.stop()
        print("Task Manager stopped successfully.")
