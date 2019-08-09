# Lab01
Project created with [Python3.7](https://www.python.org/downloads/)  
To install python, follow the [links](https://realpython.com/installing-python/)
# SUMMARY
#### What we need to cover:
* __Presentation__ :
    * The Python Philosophy
    * Fundamentals
    * Python vs the World
* __Practice__ :
    * Installation and enviroment
    * Modules and Packages: Using and Creating
    * Basic Data Types
    * Typing (mypy)
    * Data Structures (Lists, Tuples, Dictionaries, Sets)
    * Branching Statements
    * Looping Statements
    * List and Set Comprehensions
    * Functions
    * Regular Expressions
    * Lambda, map, filter and reduce
    * Exception handling
    * Context Managers
    * Decorators <Force use cases>
    * Generators <Force use cases>
    * File Handling <Persist state>
    * Multiprocessing
    * Socket
    * Third party libs
## Virtualenv
#### To create a virtualenv 
```shell
python3 -m venv venv
```
ps: the first venv in the cmd is the module use to create virtualenv, and the second venv is the name of the virtualenv 
#### To activate the virtualenv previously created
```shell
venv/bin/acivate
```
You will see __(venv)__ in the terminal
## Pip
__pip__ is the package installer for __Python__, It's installed by default with Python
#### Install necessary packages for the project
In the terminal, run:
```shell
pip install -r requirements.txt
```
## Run the script
```shell
python main.py
```

