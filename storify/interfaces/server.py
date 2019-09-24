import socket
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Thread, local

from storify.store import Store

HOST = '127.0.0.1'
PORT = 65432

local = local()


class StoreServer(Thread):
    def __init__(self, store: Store):
        self.__closed = False
        self.__conns = []
        self.__pool = ThreadPoolExecutor(max_workers=3)

        from storify.interfaces.repl import CustomerREPL
        self.__cmds = CustomerREPL(store)

        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.bind((HOST, PORT))
        super().__init__()

    def run(self):
        while not self.__closed:
            self.__sock.listen()
            conn, addr = self.__sock.accept()
            conn.setblocking()
            self.__conns.append(conn)
            print('\nCustomer connected', addr)
            self.__pool.submit(self._serve_client, conn, self.__cmds)

    def close(self):
        self.__closed = True

        for conn in self.__conns:
            conn.close()

        self.__sock.shutdown(socket.SHUT_RDWR)
        self.__sock.close()

        self.__pool.shutdown()

    @staticmethod
    def _serve_client(conn, cmds):
        local.conn = conn
        with conn:
            while True:
                try:
                    print('pre recv')
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

                    print('post send')
                except Exception:
                    conn.close()


def get_patched_input():
    def patched(value):
        if hasattr(local, 'conn'):
            local.conn.sendall(value.encode('utf-8'))
            return local.conn.recv(1024)
        else:
            input(value)

    return patched


def get_patched_print():
    def patched(value):
        if hasattr(local, 'conn'):
            local.conn.sendall(f'{value}\n'.encode('utf-8'))
        else:
            print(value)

    return patched
