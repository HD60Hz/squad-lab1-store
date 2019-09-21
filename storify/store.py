from collections import namedtuple
from concurrent.futures.thread import ThreadPoolExecutor
from functools import partial
from threading import Lock
from typing import List

from apscheduler.schedulers.background import BackgroundScheduler

from storify.scraper import Home24Scraper, Home24Categories

Product = namedtuple("Product", ["name", "price", "quantity"])


class Store:
    def __init__(self, name: str):
        self.name = name
        self.__inventory = []
        self.__items_count = 0
        self.__scheduler = None

        from storify.db.inventory import InventoryFileDB, Types
        self.__inventory_db = InventoryFileDB(Types.CSV)

        db_data = self.__inventory_db.load_products()
        if db_data:
            for product in db_data:
                self.add_product(*product)
        else:
            def push_from_home24(store: Store, lock, category: Home24Categories):
                print(f"Retrieving from Home24 : {category.name} ...")
                articles = Home24Scraper(category).retrieve_articles()
                for article in articles:
                    with lock:
                        store.add_product(*article)

                with lock:
                    store.save_inventory()

            lck = Lock()
            executor = ThreadPoolExecutor(max_workers=3)
            executor.map(partial(push_from_home24, self, lck), Home24Categories)

        self._register_autosave()

    def _register_autosave(self):
        self.__scheduler = BackgroundScheduler()
        self.__scheduler.add_job(self.save_inventory, 'interval', seconds=10)
        self.__scheduler.start()

    def close(self):
        self.__scheduler.shutdown()

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
