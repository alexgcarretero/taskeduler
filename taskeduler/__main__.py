import traceback
from sys import argv

from taskeduler import schedule

"""
If the module is run as a proper module: python3 -m taskeduler /path/to/yaml_file.yaml

It will parse that input YAML file and run a TaskManager that will be executing the
described tasks 24/7 nonstop.
"""

USAGE = "python3 -m scheduler yaml_file"


def usage_error(extra_message: str=""):
    if extra_message:
            extra_message = f"\n{extra_message}"
    print(f"USAGE: {USAGE}{extra_message}")


def main():
    """Create a TaskManager and manage the errors if necessary."""
    # Create the TaskManager, and schedule the tasks
    try:
        try:
            yaml_file = argv[1]
            task_manager = schedule(yaml_file)
        except (IndexError, FileNotFoundError) as e:
            usage_error(str(e))
            return -1
    except Exception:
        traceback.print_exc()
        return 1
    
    # Run the loop
    try:
        task_manager.loop.start(in_thread=False)
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
