from sys import argv

from taskeduler import scheudle


def with_prev_taskmanager(task_manager: 'TaskManager'):
    # Here goes some code
    ...

    # Load the yaml file into the TaskManager
    my_yaml_file = ...
    try:
        task_manager = scheudle(yaml_file=my_yaml_file, task_manager=task_manager)
    except (IndexError, FileNotFoundError) as e:
        print(f"Some error {e}")
    
    task_manager.loop.start()
    
    # More code where I can use the task_manager
    ...

def without_prev_taskmanager():
    # Here goes some code
    ...

    # Load the yaml file into the TaskManager
    my_yaml_file = ...
    try:
        task_manager = scheudle(yaml_file=my_yaml_file)
    except (IndexError, FileNotFoundError) as e:
        print(f"Some error {e}")
    
    task_manager.loop.start()
    
    # More code where I can use the task_manager
    ...
