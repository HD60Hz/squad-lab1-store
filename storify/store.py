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
        self.__inventory_db = InventoryFileDB(Types.CSV)

        db_data = self.__inventory_db.load_products()
        products = db_data or (Product(*a) for a in Home24Scraper().retrieve_articles())
        for product in products:
            self.__inventory.append(product)
            self.__items_count += product.quantity

        if not db_data:
            self.save_inventory()

    def add_product(self, name: str, price: float, quantity: int) -> Product:
        try:
            price = float(price)
            quantity = int(quantity)

        except ValueError:
            raise ValueError(f'Invalid product input : {name}, {price}, {quantity}')

        new = Product(name, price, quantity)
        self.__inventory.append(new)
        self.__items_count += new.quantity

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
