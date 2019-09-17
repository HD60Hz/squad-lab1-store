import csv
import json
import os
from enum import Enum
from typing import Iterable

from storify.store import Product


class Types(Enum):
    CSV = "csv"
    JSON = "json"


class InventoryFileDB:
    file_name = "inventory"

    def __init__(self, dir_path: str, file_type: Types = Types.CSV):
        if file_type not in Types:
            raise ValueError("Error: Invalid inventory database file type")

        if not (os.path.isdir(dir_path) and os.access(dir_path, os.W_OK)):
            raise Exception("Error: Invalid inventory database directory path")

        self.__dir_path = dir_path
        self.__file_type = file_type

    def save_products(self, products: Iterable[Product]):
        path = os.path.join(self.__dir_path, f"{self.file_name}.{self.__file_type.value}")

        if self.__file_type == Types.CSV:
            self._save_csv_products(path, products)
        else:
            self._save_json_products(path, products)

    def _save_csv_products(self, file_path, products: Iterable[Product]):
        with open(file_path, 'w') as inventory:
            for product in products:
                writer = csv.writer(inventory)
                writer.writerow(product)

    def _save_json_products(self, file_path, products: Iterable[Product]):
        with open(file_path, 'w') as inventory:
            inventory.write(json.dumps(products))

    def load_products(self) -> Iterable[Product]:
        path = os.path.join(self.__dir_path, f"{self.file_name}.{self.__file_type.value}")

        if not os.path.exists(path):
            return []

        if self.__file_type == Types.CSV:
            return self._load_csv_products(path)

        if self.__file_type == Types.JSON:
            return self._load_json_products(path)

    def _load_csv_products(self, file_path: str):
        with open(file_path, 'r') as inventory:
            reader = csv.reader(inventory)
            for product in reader:
                yield Product(product[0], float(product[1]), int(product[2]))

    def _load_json_products(self, file_path):
        with open(file_path, 'r') as inventory:
            products = json.loads(inventory.read())
            for product in products:
                yield Product(product[0], float(product[1]), int(product[2]))
