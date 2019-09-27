import socket
from threading import Thread, local

from storify.interfaces.repl import CustomerREPL
from storify.utils.server import patch_input, patch_print

local = local()
patch_input(local)
patch_print(local)

HOST = ''
PORT = 65432


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
