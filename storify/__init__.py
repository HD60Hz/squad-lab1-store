from storify.interfaces.repl import StoreREPL
from storify.store import Product, Store


def main():
    store = Store(
        name="OPEN Store",
        inventory=[
            Product("screen", 600.0, 3),
            Product("mouse", 40, 10)
        ]
    )
    StoreREPL(store).cmdloop()
