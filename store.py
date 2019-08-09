from collections import namedtuple

Product = namedtuple('Product', ['name', 'price', 'quantity'])
store = {
    'name': "",
    'inventory': []
}


def create_store(name: str):
    store["name"] = name
    return store


def create_inventory_product(name, price, quantity=0) -> Product:
    return Product(name, price, quantity)


def get_store():
    return store
