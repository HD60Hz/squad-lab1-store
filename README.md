LAB1 SQUAD TRAINING - PYTHON
---

### Files
Until now, the manager had to start the storify application and keep it running to avoid losing the inventory data. In fact, all the data added or changed in the different use cases is stored in memory. So in case of an exit, everything is lost  
In this chapter, we will improve our system by adding a file based persistance for the inventory. The file types that will be used are **CSV** and **JSON**.
Let's get started !

#### Inventory File DB
First of all we have to update our project structure by adding a ``db`` package

Result:
<pre>
storify
    ├── db
    │   ├── inventory.py
    ...
</pre>

``inventory.py`` contains database implementations to store an inventory. We will focus on the file implementation for now

```python
from enum import Enum, unique
from storify import DATA_DIR

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
```
Because we want to support multiple types of file. The ``Types`` [Enum](https://docs.python.org/3/library/enum.html) is a class definition that allows the listing, referencing and hinting of file types that will be used, for example in ``InventoryFileDB`` instantiation

To create the database, we need to provide some configuration like the above mentioned file type   
We will come back to it later but let's assume the existence of ``DATA_DIR`` that contains the path to the application data directory

For sake of simplicity, we will restrict the api of the database to: ``save_products`` and ``load_products``

##### Save products
Saving data to a CSV or a JSON file are technically different operations. Hence, it is a good practice to separate the implementation version then delegate accordingly based on the configuration    
The configuration allows us also to resolve the path of the storage file: by concatenating the directory path, the file name defined as class attribute of ``InventoryFileDB`` and file extension (csv or json). The resolved path can be communicated as argument to subroutines:``save_csv_products``, ``save_json_products``

The _path_ of the _os_ standard module can help us manage files and directories paths (verification, access, composition...)  
In our case we need to construct the path to the file that will contains our data from: directory path, file name and file extension 

```python
    ...
    import os
    ...
    def save_products(self, products: Iterable[Product]):
        path = os.path.join(self.__dir_path, f"{self.file_name}.{self.__file_type.value}")

        if self.__file_type == Types.CSV:
            self._save_csv_products(path, products)
        else:
            self._save_json_products(path, products)
    ...
```

``json`` Python builtin module provide some simple functions to marshell (``dump``/``dumps``) and unmarshell (``load``/``loads``) Python objects into/from json formatted strings

``csv`` Python builtin module allows the creation of writers and readers from IO file objects (for example returned by ``open``). The writer can write headers and rows in the targeted CSV file. The reader is an iterable that can load the file rows

```python
    ...
    import json
    import csv
    ...
    from typing import Iterable
    ...
    from storify.store import Product
    ...
    @staticmethod
    def _save_csv_products(file_path: str, products: Iterable[Product]):
        with open(file_path, 'w') as inventory:
            writer = csv.writer(inventory)
            writer.writerows(products)

    @staticmethod
    def _save_json_products(file_path: str, products: Iterable[Product]):
        with open(file_path, 'w') as inventory:
            inventory.write(json.dumps(products))
    ...
...
```

##### Load products
Similarly to saving products, loading product must verify the existence of either a CSV or JSON file based on configuration then load data from them   
We need to separate the implementation versions (CSV, JSON) then invoke the appropriate one

```python
    from typing import Iterable, Optional
    ...
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
                yield Product(product[0], float(product[1]), int(product[2]))

    @staticmethod
    def _load_json_products(file_path: str):
        with open(file_path, 'r') as inventory:
            products = json.loads(inventory.read())
            for product in products:
                yield Product(product[0], float(product[1]), int(product[2]))
```

``load_products`` returns a generator (kind of iterator) that will yield one product at a time and thus save some memory in CSV's case (JSON require loading all file content to have a valid and deserializable string)

#### Persistence of store inventory
Let's specify a simple workflow for the persistence and loading of the store inventory. We will assume that when a store is created, it will automatically load its inventory from the file database (No need for the initial/provided inventory). On the other hand we will assume, and this is for simplicity purposes, that exiting the REPL will trigger the persistance of all the inventory

```python
class Store:
    def __init__(self, name: str):
        self.name = name
        self.__inventory = []
        self.__items_count = 0

        from storify.db.inventory import InventoryFileDB, Types
        self.__inventory_db = InventoryFileDB(Types.JSON)

        products = self.__inventory_db.load_products() or []
        for product in products:
            self.__inventory.append(product)
            self.__items_count += product.quantity
```

In the ``__init__`` method, we instantiate an inventory file database by providing a hardcoded file type. This database is then kept as a store attributes for future persistence

Maybe some of you have noticed the import inside ``__init__`` (yeah import can be everywhere). The reason is to avoid _circular dependencies_ (``store`` imports ``InventoryFileDB`` while ``db/inventory`` imports ``Product``)   
Normally circular dependencies are sign of bad design. It usually means that we can find a better design where the depend and the dependency can be joined in the same module. In our case, the solution above is good enough

Because ``load_products`` return a generator we can simply iterate over the result to populate our inventory

To allow the REPL to save on exit, we will add ``save_inventory`` to store api

```python
...
def save_inventory(self):
    self.__inventory_db.save_products(self.__inventory)
```

and call it from REPL

```python
def do_exit(self, args):
    """Exit store"""
    self.__store.save_inventory()
    return True
```

Finally we need to quickly adapt the ``main`` function...BUT WAIT !
Remember, we did not yet define the ``DATA_DIR``. We intend to create a ``data`` directory in root of the project to contain all inputs/outputs of our application. Of course this new directory should not be versioned. So add it to ``.gitignore`` file

```python
from pathlib import Path
...
ROOT_DIR = Path(__file__).parents[1]
DATA_DIR = ROOT_DIR / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)

def main():
    store = Store(name="OPEN Store")
    StoreREPL(store).cmdloop()
```

``pathlib`` is a much "elegant" library to manage path than ``os.path``

Let's test ALL of this now
* Clear any inventory file (CSV, JSON)
* Start storify and list inventory to show it is empty
* Add product
* Exit storify
* Verify the existance of the inventory file
* Restart storify and list inventory to show it contains 1 product

Result:
<pre>
Welcome to OPEN Store store. Type help or ? to list commands.

Store>list_inventory

Store>add_product
Add new product...
Name> Chocolate
Price> 40
Quantity> 10
Store>exit

Process finished with exit code 0
</pre>

New file created  

Result (file system):
<pre>
data
    ├── inventory.csv
</pre>
with content
<pre>
Chocolate,40.0,10
</pre>

Restarting storify

Result:
<pre>
Welcome to OPEN Store store. Type help or ? to list commands.

Store>list_inventory
    name         price    quantity
--  ---------  -------  ----------
 0  Chocolate       40          10
Store>
</pre>