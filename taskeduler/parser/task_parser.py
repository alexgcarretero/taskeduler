import os
import re
import yaml
import importlib.util

from taskeduler.task import Task
from taskeduler.scheduler import Scheduler, ExecutionRulesManager


class TaskParser:
    """
    This class handles the parsing of the YAML files, transforming the data into Tasks.

    Args:
        task_file(str): The path to the filename to parse.
    """
    def __init__(self, task_file: str):
        self.task_file = task_file
        self.tasks = self.parse_tasks(task_file)
    
    @staticmethod
    def parse_yaml(yaml_file: str, resolve_environment: bool=True) -> dict:
        """This function loads the YAML into a dict"""
        with open(yaml_file) as f:
            yaml_string = f.read()
        
        if resolve_environment:
            yaml_string = re.sub(
                pattern=r"\$\{(\w+)\}",
                repl=lambda match: os.environ.get(match.group(1), ""),
                string=yaml_string
            )
        return yaml.safe_load(yaml_string)
    
    def parse_tasks(self, task_file: str) -> dict:
        """
        This method transforms the data in the yaml file to a dictionary (str, Task)
        with the names of the tasks and the proper tasks.
        """
        if task_file is None:
            task_file = self.task_file
        
        data = self.parse_yaml(task_file)
        tasks = {}

        for task_name, task_info in data.items():
            # Extract the task data
            file_to_import = task_info['script']['file']
            entrypoint_name = task_info['script']['entrypoint']
            entrypoint_args = task_info['script'].get('args', [])
            entrypoint_kwargs = task_info['script'].get('kwargs', {})
            scheduler_rules = task_info['repeat'].get('execution_rules', {})

            # Import the entrypoint
            module_name, _ = os.path.splitext(os.path.basename(file_to_import))
            spec = importlib.util.spec_from_file_location(name=module_name, location=file_to_import)
            module = importlib.util.module_from_spec(spec=spec)
            spec.loader.exec_module(module)
            entrypoint = getattr(module, entrypoint_name)

            for scheduler_frequency in task_info['repeat']['frequency']:
                # Create the task, and add it to the task dict
                tasks[f"{task_name}_{scheduler_frequency}"] = Task(
                    scheduler=Scheduler(
                        frequency=scheduler_frequency,
                        execution_rules_manager=ExecutionRulesManager(**scheduler_rules)
                    ),
                    task=entrypoint,
                    args=entrypoint_args,
                    kwargs=entrypoint_kwargs
                )
        return tasks
