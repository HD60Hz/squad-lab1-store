LAB1 SQUAD TRAINING - PYTHON
---

### Python

* What is Python ?  
    - Programming language created by Guido van Rossum in 1991
    - Interpreted
    - High level
    - General-purpose
    - Multi programming paradigms
    - Extensible (generally with C extensions)
    - Garbage-collected

* Why use Python ?  
    - Simple to read and **FAST** to write (Faster development cycles)
    - Open source implementations and large community
    - Rich standard library and even richer third-party modules
    - Portability
    - Fast enough for a lot of use cases (Alternative for use cases where speed is important for later)

### Installation

#### Python
First we need to have _Python_ in our environment.
To check if and what version is already installed run command:

```shell script
python --version
```

Result: 
<pre>
Python 3.7.3
</pre>

> If Python is not installed, follow this [Tutorial](https://realpython.com/installing-python/)  
> For this lab we are using Python version > 3.6 

#### PIP
To manage your Python package, you need a package manager. The most popular one is [PIP](https://pip.pypa.io/en/stable/)

> _PIP_ is a recursive acronym that stands for "Pip Installs Packages"

Starting from Python version **3.4**, PIP is included by default in Python installers  
To verify that PIP is installed, run command:

```shell script
pip --version
```

Result: 
<pre>
pip 19.1.1 from /usr/local/lib/python3.7/site-packages/pip (python 3.7)
</pre>

PIP can install packages from:  
- VCS project URLs
- Local project directories
- Local or remote source archives
- Remote repositories called indexes... most known one is [PyPI](https://pypi.org/) (Python Package Index)

When a package is installed with PIP, it will put the package files in _Python global package directories_ (e.g. site-packages)  
Let's install for example a simple package [cowsay](https://pypi.org/project/cowsay/) using the command: 

```shell script
pip install cowsay
```

Result:
> Collecting cowsay
> Using cached https://files.pythonhosted.org/packages/d4/68/af23fbf90493044fc2ea83cd62923b9952c2d38eeeab83e0c016706bfbc8/cowsay-2.0.3-py2.py3-none-any.whl
> Installing collected packages: cowsay
> Successfully installed cowsay-2.0.3

```shell script
ls /usr/local/lib/python3.7/site-packages
```

Result:
<pre>
...
cowsay
cowsay-2.0.3.dist-info
...
</pre>

The problem with the Python packages/modules resolution strategy is that all projects present in the machine will share the **same packages versions**

### VENV

[VENV](https://docs.python.org/3/library/venv.html) is a python package that can be use to encapsulate each project in its bubble
with its own _Python and PIP binaries_, hence its own site packages directories

Starting from Python version **3.3**, _VENV_ is included by default in Python installers

To create a new virtual env run command:

```shell script
python -m venv venv
```

Result (file system):
<pre>
venv
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

Your virtual environment is created... **BUT** not activated. To activate your venv run command:

```shell script
source venv/bin/activate
```

Result (shell):

<pre>
(venv) Project $
</pre>

The **(venv)** indicate that you are in the _Python virtual environment_, This means that now all installed packages will be local to the project

To deactivate your virtual env, run command:

```shell script
deactivate
```

Result:
<pre>
Project $
</pre>

#### Hello World

Now that we installed Python and activated our virtual environment... Shall we create a Hello Word program ?

Start by creating a ``main.py`` in your project directory (root) with this content:

```python
print("HELLO WORLD")
```

Then run command:

```shell script
python main.py
```

Result:

<pre>
HELLO WORLD
</pre>

Do you remember the package we installed as an example: _cowsay_? Let's try using it to say **Hello World**

Change your ``main.py`` content to:

```python
import cowsay

cowsay.tux("Hello World")
```

Result:
<pre>
Traceback (most recent call last):
File "< stdin >", line 1, in < module >
ModuleNotFoundError: No module named 'cowsay'
</pre>

Oops!... as said earlier the package was installed in the global Python package directory before we created our venv. This means that we need to reinstall it again in our venv package directory

> You should know how to do it yourself by now!

Let's re-run the command 

Result:

<pre>
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
              
</pre>
