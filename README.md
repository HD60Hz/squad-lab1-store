LAB1 SQUAD TRAINING - PYTHON
---

### Remote customer
Well the customer simulation is a success. It is time to open the store for real customers
We will create a new interface as socket server and we will allow any **telnet** user to shop from our store  
Because we do not want to go through the tedious task of rewriting a new customer REPL with sockets. We will try **Monkey Patching**

#### Socket server
Simply put, sockets are used to send messages between process across a network. This network can be local (ex: kernel) or connecting multiple hosts

In Python, the standard library _socket_ offers the necessary API to create programs connected by socket (All kind of sockets). For this lab we will use TCP sockets because there are the most suitable of our use case (Reliability)

Let's create our ``server`` module in the ``interfaces`` package

Result (file system):
<pre>
storify
    ├── ...
    ├── interfaces
    │   ├── repl.py
    │   └── server.py
    ...
</pre>

First we will start simple and create a socket server that will allow the connection of 1 customer and respond with a formated version of what ever the customer sent

```python
import socket

HOST = '127.0.0.1'
PORT = 65432

class StoreServer:
    def __init__(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind((HOST, PORT))
        self.__sock.listen()

        with self.__sock:
            conn, addr = self.__sock.accept()
            print('\nCustomer connected', addr)
            self._serve_client(conn)

    @staticmethod
    def _serve_client(conn):
        with conn:
            while True:
                command = conn.recv(1024)
                if not command:
                    break

                conn.sendall(f'You requested : {command.decode("utf-8").strip()}\n'.encode('utf-8'))
```

The sequence for creating and opening a socket then responding goes as follows:
* Create a TCP socket for the internet family address (IPv4)
* Bind the socket to the network interface and port. in this case the loopback interface and the port 65432
* Start listening to connections requests
* In the case of a connection request, accept it and start serving it
* For as long as the connection holds (No exception raised), receive the customer message (command) and send a response

When the server closes the connection, the TCP protocol dictates that the process must be kept in ``TIME_WAIT`` state waiting for any late messages from the client.
The problem is we can not restart our store server while the timeout period is not finished (address taken). This is why we use the option ``SO_REUSEADDR`` to force the kernel to bind to the used address anyway

In our ``main`` function

```python
...
from storify.interfaces.server import StoreServer
...
def main():
    store = Store(name="OPEN store")
    StoreServer()
    StoreREPL(store).cmdloop()
    store.close()
```

Let's test it. As the customer we are going to use ``telnet``

```shell script
telnet 127.0.0.1 65432
```

Result (server):
<pre>
Customer connected ('127.0.0.1', 33360)
Welcome to OPEN store store. Type help or ? to list commands.

Store>
</pre>

Result (client):
<pre>
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
HELLO
You requested : HELLO
WORLD
You requested : WORLD
^]
telnet>
Connection closed.
</pre>

Maybe you did notice that the store REPL did not start until the customer ended his session. This problem can be solved with threads

```python
from threading import Thread
...
class StoreServer(Thread):
    def __init__(self):
        super().__init__()
        self.__sock = None

    def run(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind((HOST, PORT))
        self.__sock.listen()

        with self.__sock:
            conn, addr = self.__sock.accept()
            print('\nCustomer connected', addr)
            self._serve_client(conn)

    @staticmethod
    def _serve_client(conn):
        with conn:
            while True:
                command = conn.recv(1024)
                if not command:
                    break

                conn.sendall(f'You requested : {command.decode("utf-8").strip()}\n'.encode('utf-8'))
```

The thread can be started in the main function. We use the daemon mode to allow the program to exit without waiting for these thread (We don't care if they are kill suddenly)

```python
...
def main():
    store = Store(name="OPEN store")
    server = StoreServer()
    server.daemon = True
    server.start()
    StoreREPL(store).cmdloop()
    store.close()
```

Now we can serve the customer while, we manage the store  
Still we have an other problem. If another customer connects to the server he won't be served. To add multi-client serving we add a layer of threads (one per customer)

```python
class StoreServer(Thread):
    def __init__(self):
        super().__init__()
        self.__sock = None

    def run(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind((HOST, PORT))
        self.__sock.listen()

        with self.__sock:
            while True:
                conn, addr = self.__sock.accept()
                print('\nCustomer connected', addr)
                th = Thread(target=self._serve_client, args=(conn,))
                th.daemon = True
                th.start()

    @staticmethod
    def _serve_client(conn):
        with conn:
            while True:
                command = conn.recv(1024)
                if not command:
                    break

                conn.sendall(f'You requested : {command.decode("utf-8").strip()}\n'.encode('utf-8'))
```

Its working flawlessly !

#### Current customer REPL
If we pay close attention to the current REPL. We will notice that every interaction is done through **stdout** and **stdin** respectively using **print** and **input**  
Imagine if we can change the behavior of input/print so that they use sockets instead of the standard IO streams and fallback to defaults when managing the store  

We know that a CustomerREPL object contains all the methods to handle customer use cases. But, because we don't know how _cmdloop_ of Cmd module works, we have to create our own loop and start the handler manually. The monkey patching will do the rest for us  
Let's implement our commands loop first 

```python
from storify.interfaces.repl import CustomerREPL
...
class StoreServer(Thread):
    def __init__(self, store):
        super().__init__()
        self.__sock = None
        self.__cmds = CustomerREPL(store)

    def run(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind((HOST, PORT))
        self.__sock.listen()

        with self.__sock:
            while True:
                conn, addr = self.__sock.accept()
                print('\nCustomer connected', addr)
                th = Thread(target=self._serve_client, args=(conn, self.__cmds))
                th.daemon = True
                th.start()

    @staticmethod
    def _serve_client(conn, cmds):
        with conn:
            while True:
                command = conn.recv(1024)
                if not command:
                    break

                handler_name = 'do_{cmd}'.format(cmd=command.decode('utf-8').strip().lower())
                if handler_name == 'do_exit':
                    break

                handler = getattr(cmds, handler_name, None)
                if handler:
                    handler(None)
                else:
                    conn.sendall('Unknown command\n'.encode('utf-8'))
```

Now when a customer chooses a command, nothing happens in his side but the use case is started store side  
Let's continue with our monkey patching. Create a utility module

Result (file system):
<pre>
storify
    ├── ...
    └── utils
        └── server.py
</pre>

So this is our strategy. We will create a local storage for each serving thread and at the beginning of the task we put the socket connection in it. 
When executing, our patched input/print function will look inside the local storage of the currently running thread and see if a connection is there. If so, we will know we are in the serving thread and we can use the socket to send and receive data. Otherwise, it is the main thread (without socket connection) so we fall back to the originals  

In the utility, we will use the _builtin_ module to do the patching

```python
import builtins

original_input = input
original_print = print


def patch_input(local):
    def patched(*args, **kwargs):
        if hasattr(local, 'conn'):
            msg = args[0] or ''
            local.conn.sendall(msg.encode('utf-8'))
            return local.conn.recv(1024)
        else:
            return original_input(*args, **kwargs)

    builtins.input = patched


def patch_print(local):
    def patched(*args, **kwargs):
        if hasattr(local, 'conn'):
            msg = args[0] or ''
            local.conn.sendall(f'{msg}\n'.encode('utf-8'))
        else:
            original_print(*args, **kwargs)

    builtins.print = patched
```

To finish this, we need to patch in the ``server`` module to provide the local storage

```python
...
from threading import Thread, local
...
from storify.utils.server import patch_input, patch_print

local = local()
patch_input(local)
patch_print(local)

HOST = '127.0.0.1'
PORT = 65432
...
class StoreServer(Thread):
    ...
    @staticmethod
    def _serve_client(conn, cmds):
        local.conn = conn
        with conn:
            ...
```

PERFECT !! Customers can shop remotely now

One final thing. If you want to allow friends to shop in your store from different machines in your local network, just put an empty string as the HOST

**Our application is complete. Good job and thank you for attending this LAB**


