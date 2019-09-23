import csv
import json
import os
from enum import Enum, unique
from typing import Iterable, Optional

from storify import DATA_DIR
from storify.store import Product


@unique
class Types(Enum):
    CSV = "csv"
    JSON = "json"


class InventoryFileDB:
    file_name = "inventory"

    def __init__(self, file_type: Types = Types.CSV):
        if file_type not in Types:
            raise ValueError("Error: Invalid inventory database file type")

        self.__dir_path = DATA_DIR
        self.__file_type = file_type

    def save_products(self, products: Iterable[Product]):
        path = os.path.join(self.__dir_path, f"{self.file_name}.{self.__file_type.value}")

        if self.__file_type == Types.CSV:
            self._save_csv_products(path, products)
        else:
            self._save_json_products(path, products)

    @staticmethod
    def _save_csv_products(file_path: str, products: Iterable[Product]):
        with open(file_path, 'w') as inventory:
            writer = csv.writer(inventory)
            writer.writerows(products)

    @staticmethod
    def _save_json_products(file_path: str, products: Iterable[Product]):
        with open(file_path, 'w') as inventory:
            inventory.write(json.dumps(products))

    def load_products(self) -> Optional[Iterable[Product]]:
        path = os.path.join(self.__dir_path, f"{self.file_name}.{self.__file_type.value}")

        if not os.path.exists(path):
            return None

        if self.__file_type == Types.CSV:
            return self._load_csv_products(path)

        if self.__file_type == Types.JSON:
            return self._load_json_products(path)

    @staticmethod
    def _load_csv_products(file_path: str):
        with open(file_path, 'r') as inventory:
            reader = csv.reader(inventory)
            for product in reader:
                yield Product(int(product[0]), product[1], float(product[2]), int(product[3]))

    @staticmethod
    def _load_json_products(file_path: str):
        with open(file_path, 'r') as inventory:
            products = json.loads(inventory.read())
            for product in products:
                yield Product(int(product[0]), product[1], float(product[2]), int(product[3]))
