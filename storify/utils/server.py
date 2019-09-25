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
