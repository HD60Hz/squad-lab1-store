from cmd import Cmd

from tabulate import tabulate

from storify.store import Store, OutOfStockException


class StoreREPL(Cmd):
    prompt = '<Store>'

    def __init__(self, store: Store):
        self.__store = store
        self.intro = f'Welcome to {store.name} store. Type help or ? to list commands.\n'
        super().__init__()

    def do_list_inventory(self, args):
        """List inventory"""
        print(tabulate(self.__store.inventory.values(), headers='keys'))

    def do_add_product(self, args):
        """Add new product to inventory"""
        print('Add new product...')

        name = input('Name> ')
        price = input('Price> ')
        quantity = input('Quantity> ')

        try:
            self.__store.add_product(name, price, quantity)

        except ValueError:
            print('Error: You must provide a valid product')

    def do_remove_product(self, args):
        """Remove existing product from inventory"""
        try:
            id = int(input('Choose a product> '))
            removed = self.__store.inventory[id]

            self.__store.remove_product(removed)
            print(f'Product has been removed : {removed!r}')

        except (KeyError, ValueError):
            print('Error: You must provide an existing product id')

    def do_modify_product(self, args):
        """Modify existing product in inventory"""
        try:
            id = int(input('Choose a product> '))
            modified = self.__store.inventory[id]

        except (KeyError, ValueError):
            print('Error: You must provide an existing product id')
            return

        print(f'Modify product : {modified!r}')
        name = input(f'Name [{modified.name}]> ') or modified.name
        price = input(f'Price [{modified.price}]> ') or modified.price
        quantity = input(f'Quantity [{modified.quantity}]> ') or modified.quantity

        try:
            self.__store.update_product(modified, name, price, quantity)

        except ValueError:
            print('Error: You must provide a valid product')

    def do_exit(self, args):
        """Exit store"""
        self.__store.save_inventory()
        return True

    def do_simulate_customer(self, args):
        CustomerREPL(self.__store).cmdloop()


class CustomerREPL(Cmd):
    prompt = "<Customer>"

    def __init__(self, store: Store):
        self.__store = store
        self.__cart = self.__store.create_cart()
        super().__init__()

    def do_list_inventory(self, args):
        """List inventory"""
        print(tabulate(self.__store.inventory.values(), headers='keys'))

    def do_list_cart(self, args):
        """List products in cart"""
        for product, quantity in self.__cart.content:
            print(f'{product.id} {product.name} {product.price} x {quantity}')

    def do_pick_product(self, args):
        """Adding inventory product to customer cart"""
        try:
            id = int(input('Choose a product> '))
            picked = self.__store.inventory[id]

        except (KeyError, ValueError):
            print('Error: You must provide an existing product id')
            return

        print(f'Picking product : {picked}')
        quantity = input('How many? ')

        try:
            self.__cart.pick_product(picked, quantity)

        except ValueError:
            print('Error: You must provide a valid quantity')

    def do_discard_product(self, args):
        """Removing inventory product to customer cart"""
        try:
            id = int(input('Choose a product> '))
            discarded = self.__store.inventory[id]

        except (KeyError, ValueError):
            print('Error: You must provide an existing product id')
            return

        try:
            self.__cart.discard_product(discarded)

        except ValueError:
            print('Error: Product not in cart')

    def do_checkout(self, args):
        """Checkout"""
        try:
            purchases, total = self.__store.checkout(self.__cart)

            print('You have purchased:')
            for purchase in purchases:
                print(f'{purchase.name} {purchase.price} x {purchase.quantity}')

            print(f'Total: {total}')
        except (ValueError, OutOfStockException) as e:
            print(e)

    def do_exit(self, args):
        """Exit customer session"""
        return True
