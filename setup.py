import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "readme.md").read_text()

# This call to setup() does all the work
setup(
    name="taskeduler",
    version="1.0.1",
    description="Schedule your tasks, easily",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/alexgcarretero/taskeduler",
    author="@alexgcarretero",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["taskeduler", "taskeduler.parser", "taskeduler.scheduler", "taskeduler.task", "taskeduler.utils"],
    include_package_data=True,
    install_requires=["PyYAML"],
    entry_points={
        "console_scripts": [
            "tascheduler=taskeduler.__main__:main",
        ]
    },
)
