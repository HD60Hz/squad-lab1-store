import os
from collections import namedtuple
from typing import List

Product = namedtuple("Product", ["name", "price", "quantity"])


class Store:
    def __init__(self, name: str):
        self.name = name
        self.__inventory = []
        self.__items_count = 0

        from storify.db.inventory import InventoryFileDB, Types
        dir_path = os.path.dirname(os.path.abspath(__file__))
        self.__inventory_db = InventoryFileDB(dir_path, Types.JSON)

        for product in self.__inventory_db.load_products():
            self.__inventory.append(product)
            self.__items_count += product.quantity

    def add_product(self, name: str, price: float, quantity: int):
        try:
            price = float(price)
            quantity = int(quantity)
            new = Product(name, price, quantity)
            self.__inventory.append(new)

        except ValueError:
            raise ValueError(f'Invalid product input : {name}, {price}, {quantity}')

        self.__items_count += quantity

        return new

    def remove_product(self, product: Product):
        try:
            self.__inventory.remove(product)

        except ValueError:
            raise ValueError(f'Unknown product : {product!r}')

        self.__items_count -= product.quantity

    def save_inventory(self):
        self.__inventory_db.save_products(self.__inventory)

    @property
    def inventory(self) -> List[Product]:
        return self.__inventory[:]

    @property
    def items_count(self) -> int:
        return self.__items_count
