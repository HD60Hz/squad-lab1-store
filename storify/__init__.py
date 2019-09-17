from storify.interfaces.repl import StoreREPL
from storify.store import Store


def main():
    store = Store(name="OPEN Store")
    StoreREPL(store).cmdloop()
