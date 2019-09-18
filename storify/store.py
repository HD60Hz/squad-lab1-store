import os
from collections import namedtuple
from typing import List

from storify.scraper import Home24Scraper

Product = namedtuple("Product", ["name", "price", "quantity"])


class Store:
    def __init__(self, name: str):
        self.name = name
        self.__inventory = []
        self.__items_count = 0

        from storify.db.inventory import InventoryFileDB, Types
        dir_path = os.path.dirname(os.path.abspath(__file__))
        self.__inventory_db = InventoryFileDB(dir_path, Types.CSV)

        data_exist = False
        for product in self.__inventory_db.load_products():
            data_exist = True
            self._append_inventory(product)

        if not data_exist:
            for product in Home24Scraper().retrieve_articles():
                self._append_inventory(Product(*product))
                self.save_inventory()

    def add_product(self, name: str, price: float, quantity: int):
        try:
            price = float(price)
            quantity = int(quantity)

        except ValueError:
            raise ValueError(f'Invalid product input : {name}, {price}, {quantity}')

        new = Product(name, price, quantity)
        self._append_inventory(new)

        return new

    def _append_inventory(self, product: Product):
        self.__inventory.append(product)
        self.__items_count += product.quantity

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
