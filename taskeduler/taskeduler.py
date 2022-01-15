import os
from taskeduler.task import TaskManager
from taskeduler.parser import TaskParser


def schedule(yaml_file: str, task_manager: 'TaskManager'=None, run_loop: bool=False) -> 'TaskManager':
    """Parse the yaml file and create a TaskManager (if `task_manager` is None) that runs it."""
    # Parse yaml
    if not os.path.exists(yaml_file):
        raise FileNotFoundError(f"The yaml file '{yaml_file}' does not exist.")
    task_parser = TaskParser(yaml_file)
    
    # Create TaskManager and add all tasks
    task_manager = task_manager or TaskManager()
    for task_name, task in task_parser.tasks.items():
        task_manager.add_task(task_name, task)
    
    if run_loop and not task_manager.loop.is_running():
        task_manager.loop.start()
    return task_manager
