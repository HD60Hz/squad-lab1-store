from cmd import Cmd

from tabulate import tabulate

from storify.store import Store


class StoreREPL(Cmd):
    prompt = "<Store>"

    def __init__(self, store: Store):
        self.__store = store
        self.intro = f'Welcome to {store.name} store. Type help or ? to list commands.\n'
        super().__init__()

    def do_list_inventory(self, args):
        """List inventory"""
        print(tabulate(self.__store.inventory, headers="keys", showindex=True))

    def do_add_product(self, args):
        """Add new product to inventory"""
        print("Add new product...")

        name = input("Name> ")
        price = input("Price> ")
        quantity = input("Quantity> ")

        try:
            self.__store.add_product(name, price, quantity)

        except ValueError:
            print("Error: You must provide a valid product")

    def do_remove_product(self, args):
        """Remove existing product from inventory"""
        try:
            index = int(input("Choose a product> "))
            removed = self.__store.inventory[index]

            self.__store.remove_product(removed)
            print("Product has been removed : {!r}".format(removed))

        except (IndexError, ValueError):
            print("Error: You must provide an existing product id")

    def do_modify_product(self, args):
        """Modify existing product in inventory"""
        try:
            index = int(input("Choose a product> "))
            modified = self.__store.inventory[index]

        except (IndexError, ValueError):
            print("Error: You must provide an existing product id")
            return

        print("Modify product : {!r}".format(modified))

        name = input(f"Name [{modified.name}]> ") or modified.name
        price = input(f"Price [{modified.price}]> ") or modified.price
        quantity = input(f"Quantity [{modified.quantity}]> ") or modified.quantity

        try:
            self.__store.add_product(name, price, quantity)

        except ValueError:
            print("Error: You must provide a valid product")
            return

        try:
            self.__store.remove_product(modified)

        except ValueError:
            assert False, "Unexpected Error!"

    def do_exit(self, args):
        """Exit store"""
        self.__store.save_inventory()
        return True
