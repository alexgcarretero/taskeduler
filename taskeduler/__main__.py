import os
import traceback
from sys import argv

from taskeduler.task import TaskManager
from taskeduler.parser import TaskParser

"""
If the module is run as a proper module: python3 -m taskeduler /path/to/yaml_file.yaml

It will parse that input YAML file and run a TaskManager that will be executing the
described tasks 24/7 nonstop.
"""

USAGE = "python3 -m scheduler yaml_file"


class UsageError(Exception):
    """Raised when there are errors in the usage of the module."""
    def __init__(self, extra_message: str=""):
        if extra_message:
            extra_message = f"\n{extra_message}"
        super().__init__(f"USAGE: {USAGE}{extra_message}")


def run(task_manager):
    """Parse the tasks and run them."""
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


def main():
    """Create a TaskManager and manage the errors if necessary."""
    task_manager = TaskManager()
    try:
        run(task_manager)
    except UsageError as e:
        print(e)
        return -1
    except Exception:
        traceback.print_exc()
        return 1
    except KeyboardInterrupt:
        print("Stopping all the threads and tasks...")
        print(f"This may take up to {task_manager.loop.sleep_interval} seconds...")
        task_manager.loop.stop()
        print("Task Manager stopped successfully.")
    return 0


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
