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

    @property
    def inventory(self) -> List[Product]:
        return self.__inventory[:]

    @property
    def items_count(self) -> int:
        return self.__items_count
