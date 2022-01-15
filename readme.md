# Taskeduler: schedule your tasks, easily
This module is a tool written in python built to automate tasks.

Write a python function and configure the task in a yaml file. Then it is going to be executed following the programed scheduler.

## How to schedule a task
There are two main ways to use the Taskeduler: describing the tasks in a yaml file and running the module passing the file as an argument, or embeding the module in another python project, importing the `TaskManager` and adding the tasks manually.

There are examples of both usages in the [example file](./examples).

### Via YAML file
There are 3 main elements that are reperented in the yaml file: the *task name*, the *task entrypoint* and the *task schedule*.

```yaml
my_task:
  # Here goes the entrypoint information.
  script:
    # The path to the file where the entrypoint function is defined.
    file: ${SCRIPTS_DIR}/here/lies/the/entrypoint.py
    # The proper name of the entrypoint function.
    entrypoint: my_entrypoint_function
    # The entrypoint args and kwargs if wanted.
    args:
        - first_argument
        - ...
    kwargs:
        kwarg_name: kwarg_value
        ...
  # Here goes the schedule information.
  repeat:
    # How often the task will be repeated.
    frequency: ['daily']
    # Some additional rules about when will the task be executed.
    execution_rules:
      week_day: ["mon", "tue", "wed", "thu", "fri"]
      time: ["10:00"]
```
You may note that the parsing of the YAML file will resolve environment variables if enclosed into braces, preceded with the dollar sign: `${ENV_VARIABLE}`.

All the fields shown above are mandatory except of
All the fields shown in the previous example are mandatory except `args`, `kwargs` and the proper execution rules. To read more about the execution rules, go to the [scheduler rules section](#scheduler-rules).

The frecuency and all the execution rules are ment to be iterables in the YAML definition, there will be created a task for each defined frecuency, named as *`task_name`_`frequency`*.

### Via Python code
To build the `Task` object, first is needed to create a `Scheduler`. Then, to execute the task is required to add the task to a `TaskManager`, and run the loop.

```python
>>> from taskeduler.scheduler import ExecutionRulesManager, Scheduler
>>> from taskeduler.task import Task, TaskManager
>>>
>>> # Define the entrypoint function
>>> def my_entrypoint_function(name: str) -> None:
...     print(f"Hello {name}! What's up?")
>>>
>>> # Create the Scheduler and the ExecutionRulesManager
>>> scheduler = Scheduler(
...     frecuency="daily",
...     execution_rules_manager=ExecutionRulesManager(
...         week_days=["mon", "tue", "wed", "thu", "fri"],
...         time=["10:00"]
...     )
... )
>>>
>>> # Create the task
>>> task = Task(
...     scheduler=scheduler,
...     task=greet,
...     args=("Peter",)
... )
>>>
>>> # Setup the TaskManager and run the loop
>>> task_manager = TaskManager()
>>> task_manager.add_task("test_taskeduler", task)
>>> task_manager.loop.start()
```

You can also load a YAML from the python code!

```python
>>> from taskeduler import schedule
>>> my_yaml = "/path/to/my/file.yaml"
>>> task_manager = schedule(yaml_file=my_yaml)
>>> task_manager.loop.start()
```

Even with an already existing `task_manager`:

```python
>>> from taskeduler import TaskManager, schedule
>>> task_manager = TaskManager()
>>> my_yaml = "/path/to/my/file.yaml"
>>> schedule(yaml_file=my_yaml, task_manager=task_manager)
>>> task_manager.loop.start()
```

## Scheduler rules
The **frequencies** determine the period of wait between the task executions. The **execution rules** determine some aditional *"checks"* that must be met, represented by a list of possible values.

There are 6 scheduler *frequencies* and 4 *execution rules* available:
- Scheduler Frecuencies:
    - **minutely**: Repeat every minute.
        *i.e: 10:10 => 10:11*
    - **hourly**: Repeat every hour.
        *i.e: 10:10 => 11:10*
    - **daily**: Repeat every day.
        *i.e: 11 jul => 12 jul*
    - **weekly**: Repeat every week (based on the week day).
        *i.e: monday 1 => monday 8*
    - **monthly**: Repeat every month (based on the month day).
        *i.e: January 27 => February 27; January 29 => February 29 (leap year)// March 1*
    - **yearly**: Repeat every year (based on the month day and month).
        *i.e: 20 aug 2019 => 20 aug 2020*
- Execution Rules:
    - **time**: This restriction determines the *hour* and *minute* when the task can be executed in a *HH:MM* format.
    - **month_days**: This restriction determines the *number of day in the month* when the task can be executed.
    - **week_days**: This restriction determines the *week day* when the task can be executed, in any of the following formats:
        - *full name*: monday, tuesday, ...
        - *short name*: mon, tue, ...
        - *number*: 0, 1, ...
    - **month**: This restriction determines the *month* when the task can be executed, in any of the following formats:
        - *full name*: january, february, ...
        - *short name*: jan, feb, ...
        - *number*: 1, 2, ...
