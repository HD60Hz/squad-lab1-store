LAB1 SQUAD TRAINING - PYTHON
---

### Remote customer
Well the customer simulation is a success. It is time to open the store for real and multiple customers
We will create a new interface as socket server and we will allow any **telnet** use to shop from our store  
Because we do not want to go through the tedious task of rewriting a new customer REPL with sockets. We will try **Monkey Patching**

#### Socket server
Simply put, sockets are used to send messages between process across a network. This network can be local (ex: kernel) or connecting multiple hosts

In Python, the standard library ``socket`` offers all the necessary API to create programs connect by socket (All kind of sockets)

Let's create our ``server`` module in the _interfaces_ package

```python
import socket

from storify.store import Store

HOST = '127.0.0.1'
PORT = 65432

class StoreServer:
    def __init__(self, store: Store):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind((HOST, PORT))
        self.__sock.listen()
        super().__init__()

    def run(self):
        while True:
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

                # Resolve handler
                ...

                if handler:
                    handler()
                else:
                    conn.sendall('Unknown command\n'.encode('utf-8'))
```

#### Current customer REPL
If we pay close attention to the current REPL. We will notice that  
