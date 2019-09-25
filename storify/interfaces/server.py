import socket
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Thread, local

from storify.store import Store
from storify.utils.server import patch_input, patch_print

local = local()
patch_input(local)
patch_print(local)

HOST = '127.0.0.1'
PORT = 65432


class StoreServer(Thread):
    def __init__(self, store: Store):
        self.__closed = False
        self.__conns = []
        self.__pool = ThreadPoolExecutor(max_workers=3)

        from storify.interfaces.repl import CustomerREPL
        self.__cmds = CustomerREPL(store)

        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind((HOST, PORT))
        self.__sock.listen()
        super().__init__()

    def run(self):
        while not self.__closed:
            try:
                conn, addr = self.__sock.accept()
                self.__conns.append(conn)
                print('\nCustomer connected', addr)
                self.__pool.submit(self._serve_client, conn, self.__cmds)
            except OSError as e:
                print(e)

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
