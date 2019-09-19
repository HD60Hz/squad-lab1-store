LAB1 SQUAD TRAINING - PYTHON
---

### Refactoring
Storify implementation of the last chapter was a great start into practicing Python programming. It is a small but close example to a real world app. However, even though a one file script is acceptable to target a single and low complexity problem, it is a bad practice for application developpement especially for apps relatively complex and with a futur need of evolution and scalability.

So let's see how we can refactor our code to improve it
* Seperate Interface and store
* Encapsulate store logic in an object (OOP)
* Use a command builtin library instead of our REPL implementation
* Use types annotations

#### Seperation
One way to think about the seperation is to suppose our store can be managed with multiple interfaces or can have no interface at all. They must be a loose coupling between the interfaces and the store.
More importantly, they need to have a unidirectional relationship between them. A store doesn't need to know about the existance of an application interface. However the application interface should know about, and thus, carve itself based on its logic.

Let's start by seperating storify into multiple files :

<pre>
.
├──...
└── storify
    ├── __init__.py
    ├── interfaces
    │   └── cli.py
    ├── __main__.py
    └── store.py
</pre>

Now, Storify is a package containing a subpackage for the interfaces and a store module. We moved ``create_store`` and ``Product`` definitions into ``store``  and kept the rest in ``cli`` module

The ``__init__.py`` is the initialisation file for the storify package. We can use it to define a ``main`` function that creates a store and run it in a REPL

```python
from storify.interfaces.cli import run_cli
from storify.store import create_store, Product

def main():
    store = create_store(
        name="OPEN Store",
        inventory=[
            Product("screen", 600.0, 3),
            Product("mouse", 40, 10)
        ]
    )
    run_cli(store)
```
Notice the imports statements on top. They use relative paths to modules in the form of : \<package\>.\<subpackage\>..\<module\> to import elements from them. To allow python interpreter to know the location of the packages that you import from, you need to add the location of the root of the project to python path either by ``PYTHONPATH`` environnement variable or ``sys.path``

To keep the same command (kind of) for running storify, we can use ``__main__.py`` as the entry point for the application

```python
from storify import main

if __name__ == '__main__':
    main()
```

Let's test it. run the command :

```shell
python storify
```

<pre>

==================================
      Welcome in OPEN Store
==================================
        Items count : 13

         0  -  Exit
         1  -  List inventory
         2  -  Add product
         3  -  Remove product
         4  -  Modify product
your choice> 1
</pre>

It still works !

We will continue our refactoring by encapsulating the store logic inside a class of the store module

```python
from collections import namedtuple
from typing import List

Product = namedtuple("Product", ["name", "price", "quantity"])

class Store:
    def __init__(self, name: str, inventory: List[Product] = []):
        self.name = name
        self.__inventory = [*inventory]
        self.__items_count = 0

        for product in inventory:
            self.__items_count += product.quantity

    def add_product(self, name: str, price: float, quantity: int):
        try:
            price = float(price)
            quantity = int(quantity)
            self.__inventory.append(Product(name, price, quantity))

        except ValueError:
            raise ValueError(f'Invalid product input : {name}, {price}, {quantity}')

        self.__items_count += quantity

    def remove_product(self, product: Product):
        try:
            self.__inventory.remove(product)

        except ValueError:
            raise ValueError(f'Unknown product : {product!r}')

        self.__items_count -= product.quantity

    @property
    def inventory(self) -> List[Product]:
        return self.__inventory[:]

    @property
    def items_count(self) -> int:
        return self.__items_count
```

Now the store can be created as an object.  Most importantly we encapsulated and protected the store data by hiding it and only allowing the management of the inventory through an API that validates the inputs (raising exception with comprehensive messages) and limits the actions
By the way, we dont need the factory function ``create_store`` anymore

Did you notice the use of [type hinting](https://docs.python.org/3/library/typing.html)... it is supported since version 3.5 of python and have been improved up on throught out minor releases (even 3.6 ones). It does not add any runtime behavior (mostly) and it is just a hint for type checkers and static code analysers (ex: IDE)... Not necessary but recommanded for large project, we will continue using it in our lab

Next, we have to adapt our REPL command handlers to use the new store representation. While doing this, we are going to refactor the REPL to use the builtin [``Cmd``](https://docs.python.org/3/library/cmd.html) library... We reinvented the wheel just to learn !

```python
from cmd import Cmd
from tabulate import tabulate
from storify.store import Store

class StoreCLI(Cmd):
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
            return

        except ValueError:
            print("Error: You must provide a valid product")

        try:
            self.__store.remove_product(modified)

        except ValueError:
            assert False, "Unexpected Error!"

    def do_exit(self, args):
        """Exit store"""
        return True
```

The modify product use case combines adding new product to the store and removing the old one. It is just a simplification due to the index of products not beeing important

The main function becomes :

```python
from storify.interfaces.cli import StoreCLI
from storify.store import Product, Store

def main():
    store = Store(
        name="OPEN Store",
        inventory=[
            Product("screen", 600.0, 3),
            Product("mouse", 40, 10)
        ]
    )
    StoreCLI(store).cmdloop()
```

Run the application now to see if it is working

```shell
python storify
```
Result:

<pre>
Welcome to OPEN Store store. Type help or ? to list commands.

Store>?

Documented commands (type help <topic>):
========================================
add_product  exit  help  list_inventory  modify_product  remove_product

<Store>list_inventory
    name      price    quantity
--  ------  -------  ----------
 0  screen      600           3
 1  mouse        40          10
Store>
</pre>

