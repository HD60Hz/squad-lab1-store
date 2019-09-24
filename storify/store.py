from collections import namedtuple, defaultdict
from concurrent.futures.thread import ThreadPoolExecutor
from functools import partial
from threading import Lock
from typing import Iterable, Tuple, Dict

from apscheduler.schedulers.background import BackgroundScheduler

from storify.scraper import Home24Scraper, Home24Categories

Product = namedtuple("Product", ["id", "name", "price", "quantity"])
Purchase = namedtuple("Purchase", ["name", "price", "quantity"])


class Store:
    def __init__(self, name: str):
        self.name = name
        self.__last_id = 0
        self.__inventory = {}
        self.__items_count = 0
        self.__carts = []
        self.__checked_carts = []
        self.__scheduler = None

        from storify.db.inventory import InventoryFileDB, Types
        self.__inventory_db = InventoryFileDB(Types.CSV)

        from storify.printer import InvoicePrinter
        self.__invoice_printer = InvoicePrinter(self.name)

        db_data = self.__inventory_db.load_products()
        if db_data:
            for product in db_data:
                self._index_in_inventory(product)
        else:
            def push_from_home24(store: Store, lock, category: Home24Categories):
                print(f'Retrieving from Home24 : {category.name} ...')
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

    def _index_in_inventory(self, product: Product):
        self.__inventory[product.id] = product
        self.__items_count += product.quantity
        self.__last_id = max(self.__last_id, product.id)

    def add_product(self, name: str, price: float, quantity: int) -> Product:
        try:
            price = float(price)
            quantity = int(quantity)

        except ValueError:
            raise ValueError(f'Invalid product input : {name}, {price}, {quantity}')

        self.__last_id += 1
        new = Product(self.__last_id, name, price, quantity)
        self._index_in_inventory(new)

        return new

    def remove_product(self, product: Product):
        try:
            del self.__inventory[product.id]

        except KeyError:
            raise ValueError(f'Unknown product : {product!r}')

        self.__items_count -= product.quantity

    def update_product(self, product: Product, name: str, price: float, quantity: int):
        if product.id not in self.__inventory:
            raise ValueError(f'Unknown product : {product!r}')

        try:
            price = float(price)
            quantity = int(quantity)

        except ValueError:
            raise ValueError(f'Invalid product input : {name}, {price}, {quantity}')

        self.__inventory[product.id] = Product(product.id, name, price, quantity)

    def save_inventory(self):
        self.__inventory_db.save_products(self.__inventory.values())

    def create_cart(self):
        cart = Cart(self.__inventory)
        self.__carts.append(cart)

        return cart

    def checkout(self, cart):
        if cart not in self.__carts:
            raise ValueError(f'Unknown cart: {cart!r}')

        if cart in self.__checked_carts:
            raise ValueError('Cart already checked')

        uow = []
        for product, quantity in cart.content:
            if product.quantity < quantity:
                raise Exception(f'{product!r} out of stock')

            uow.append((product, quantity))

        purchases, total = [], 0
        for product, quantity in uow:
            self.update_product(product, product.name, product.price, product.quantity - quantity)

            total += product.price * quantity
            purchases.append(Purchase(product.name, product.price, quantity))

        self.__checked_carts.append(cart)

        self.__invoice_printer.print(purchases, total)

        return purchases, total

    @property
    def inventory(self) -> Dict[int, Product]:
        return self.__inventory.copy()

    @property
    def items_count(self) -> int:
        return self.__items_count


class Cart:
    def __init__(self, inventory):
        self.__inventory = inventory
        self.__products = defaultdict(lambda: 0)  # or defaultdict(int)

    def pick_product(self, product, quantity):
        if product.id not in self.__inventory:
            raise ValueError(f'Unknown product : {product!r}')

        try:
            quantity = self.__products[product.id] + int(quantity)
        except ValueError:
            raise ValueError(f'Invalid quantity : {quantity}')

        if not (0 < quantity <= product.quantity):
            raise ValueError(f'Invalid quantity : {quantity}')

        self.__products[product.id] = quantity

    def discard_product(self, product):
        if product.id not in self.__products:
            raise ValueError(f'Unknown product : {product!r}')

        del self.__products[product.id]

    @property
    def content(self) -> Iterable[Tuple[Product, int]]:
        return ((self.__inventory[id], quantity) for id, quantity in self.__products.items())
