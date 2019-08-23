LAB1 SQUAD TRAINING - PYTHON
---

* What is Python ?  
    - Programming language created by Guido van Rossum in 1991
    - Interpreted
    - High level
    - General-purpose
    - Multi programming paradigms
    - Extensible (generaly with C extensions)
    - Garbage-collected

* Why use Python ?  
    - Simple to read and **FAST** to write (Faster development cycles)
    - Open source implementations and large community
    - Rich standard library and even richer third-party modules
    - Portability
    - Fast enough for a lot of use cases (Alternative for use cases where speed is important for later)

### Let's stop the theory and start practicing ...

### 1. PYTHON
First we need to have Python in our environment.
To check if and what version is already installed run command:
```shell
python --version
```
Result: 
> Python 3.7.3

*If Python is not installed, follow this [Tutorial](https://realpython.com/installing-python/)*...
*For this lab we are using Python version > 3.6*

### 2. PIP
To manage your python package, you need a package manager... 
The most popular one is PIP   
*FUNNY: pip is a recursive acronym that stands for "Pip Installs Packages"*

Starting from Python version 3.4...
PIP is included by default in Python installers

**SO**... 
to verify that PIP is installed, run command:
```shell
pip --version
```
Result: 
> pip 19.1.1 from /usr/local/lib/python3.7/site-packages/pip (python 3.7)

PIP can install packages from:  
- VCS project urls
- Local project directories
- Local or remote source archives
- Remote repositories called indexes... most known one is PyPI (Python Package Index)

When a package is installed with PIP using the command (example package - cowsay):
```shell
pip install cowsay
```
Result:
> Collecting cowsay   
> Using cached https://files.pythonhosted.org/packages/d4/68/af23fbf90493044fc2ea83cd62923b9952c2d38eeeab83e0c016706bfbc8/cowsay-2.0.3-py2.py3-none-any.whl   
> Installing collected packages: cowsay   
> Successfully installed cowsay-2.0.3

... the manager will put the package files in python global package directories (e.g. site-packages)
>  /usr/local/lib/python3.7/site-packages/

The problem with the strategy used by python to resolve packages and modules is that all python projects
will share the same packages versions

*SOLUTION: VIRTUAL ENVIRONMENTS*

### 3. VENV

VENV is a python package that allow us to encapsulate each project in its own bubble
with its proper python and pip binaries... and thus its own site packages directories

Starting from Python version 3.3...
VENV is included by default in Python installers

To create a new virtual env run command:
```shell
python -m venv env
```
Result: \<current directory structure\>
<pre>
env
├── bin
│   ├── activate
│   ├── activate.csh
│   ├── activate.fish
│   ├── easy_install
│   ├── easy_install-3.7
│   ├── pip
│   ├── pip3
│   ├── pip3.7
│   ├── python -> python3.7
│   ├── python3 -> python3.7
│   └── python3.7 -> /Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7
├── include
├── lib
│   └── python3.7
│       └── site-packages
└── pyvenv.cfg
</pre>

Your virtual environment is created... **BUT** not activated   
To activate your venv run command:
```shell
source env/bin/activate
```
Result:
> (env) Project $

The "(env)" indicate that you are in the python virtual environment   
Now all installed packages will be local to the project

To desactivate your venv run command (from venv):
```shell
deactivate
```
Result:
> Project $

### 4. HELLO WORLD

Now that we installed our environment and of course activated the virtual one... Shall we create a Hello Word program ?

Start by creating a ```main.py``` in your project directory (root) with content:
```python
print("HELLO WORLD")
```
Then run command:
```shell
python main.py
```
Result:
> HELLO WORLD

Do you remember the package we installed as an example: cowsay   
Let's try using it to say "Hello World"

Change your ```main.py``` content to:
```python
import cowsay

cowsay.tux("Hello World")
```
Result:
> Traceback (most recent call last):  
> File "\<stdin\>", line 1, in \<module\>  
> ModuleNotFoundError: No module named 'cowsay'

Ooops ... as said earlier the package was installed in 
the global python package directory before we created and activated our venv... 
This means that we need to reinstall it again in our venv python package directory   

*You should know how to do it yourself by now* 

Let's re-run the command again   

Result:
```
  ___________
< Hello World >
  ===========
                \
                 \
                  \            
                   .--.
                  |o_o |
                  |:_/ |
                 //   \ \
                (|     | )
               /'\_   _/`\
               \___)=(___/
              
              
```
