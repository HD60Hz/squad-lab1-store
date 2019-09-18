LAB1 SQUAD TRAINING - PYTHON
---

### Files
Until now, the manager had to start the storify application and keep it running to avoid losing the inventory data. In fact, all the data added or changed in the different use cases is stored in memory. so in case of an exit, everything is lost.
In this chapter, we will improve our system by adding a file based  persistance for the inventory. The file types that will be used are CSV and JSON.
Let's get started !

### Inventory File DB
First of all we have to update our project structure by adding a ``db`` package

<pre>
storify
    ├── db
    │   ├── inventory.py
    ...
</pre>

``inventory.py`` contains database implementation to store an inventory. We will focus on the file implementation for now

```python
import os

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
```
Because we want to support multiple types of file. The ``Types`` [Enum](https://docs.python.org/3/library/enum.html) is a class definition that allow to listing, referencing and hinting (var types) the file types that well be used (for example InventoryFileDB instanciation)

To create the file database, we need to provide some configuration like the path in the file system where to put the inventory data and inside a file of which type. Using the ``os`` module, we can validate the existance and write access of the target directory

For sake of simplicity, we will restrict the api of the database to : ``save_products`` and ``load_products``

#### Save products
Saving data to a CSV or a JSON file are technically different operations. Hence, it is a good practice to seperate the implementation version then delegate accordingly based on the configuration (chosen file type)
The configuration allows us also to resolve the path of the storage file : by concatenating the directory path, the file name defined as class attribut of InventoryFileDB and file extension (csv or json). The resolved path can be communicated as argument to subroutines :``save_csv_products``, ``save_json_products``

```python
    ...
    def save_products(self, products: Iterable[Product]):
        path = os.path.join(self.__dir_path, f"{self.file_name}.{self.__file_type.value}")

        if self.__file_type == Types.CSV:
            self._save_csv_products(path, products)
        else:
            self._save_json_products(path, products)
    ...
```

``json`` Python builtin library provide some simple functions to marshell (dump/dumps) and unmarshell (load/loads) Python objects into/from json formated strings

``csv`` Python builtin library allows the creation of writers and readers from IO file objects (``open``). The writer can write headers and rows in the targeted CSV file. The reader is an iterable that can load the file rows

```python
    ...
    @staticmethod
    def _save_csv_products(file_path: str, products: Iterable[Product]):
        with open(file_path, 'w') as inventory:
            for product in products:
                writer = csv.writer(inventory)
                writer.writerow(product)

    @staticmethod
    def _save_json_products(file_path: str, products: Iterable[Product]):
        with open(file_path, 'w') as inventory:
            inventory.write(json.dumps(products))
    ...
...
```
#### Load products
Similarly to saving products, loading product must verify the existance of either a CSV or JSON file based on configuration then load data from them, we need to seperate the implementation versions (CSV, JSON) then invoke the appropriate one

```python
...
    def load_products(self) -> Iterable[Product]:
        path = os.path.join(self.__dir_path, f"{self.file_name}.{self.__file_type.value}")

        if not os.path.exists(path):
            return []

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

``load_products`` returns a generator (kind of iterator) that will yield one product at time and thus saving some memory in the case of CSV (JSON require loading all file content to have a valid and deserializable string)

### Persistance of store inventory
Let's specify a simple workflow for the persistance and loading of the store inventory. We will assume that when a store is created (storify is started) it will automatically load its inventory from the file database. No need for the initial/provided inventory. On the other hand we will assume, and this is for simplicity purposes, that exiting the RELP with trigger the persistance of all the inventory

```python
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
```
In the init/construction method we instantiate an inventory file database by providing the absolute path of ``store`` module parent directory, aka ``storify`` and a hardcoded file type
This database is then kept as a store attributes for future persistance

Maybe some of you have noticed the import inside ``__init__`` (yeah import can be everywhere). The reason behind that is to avoid a circular dependencies (store imports InventoryFileDB, and db/inventory import Product)
Normally circular dependencies are sign of bad design. It means that there may be a better design where the depend and the dependency can joined in the same module. In our case, the solution above is good enough

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

Finally we need to quickly adapt the main function

```python
def main():
    store = Store(name="OPEN Store")
    StoreREPL(store).cmdloop()
```

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
<pre>
storify
    ├── ...
    ├── inventory.csv
</pre>
with content
<pre>
Chocolate,40.0,10
</pre>

Restarting storify

<pre>
Welcome to OPEN Store store. Type help or ? to list commands.

Store>list_inventory
    name         price    quantity
--  ---------  -------  ----------
 0  Chocolate       40          10
Store>
</pre>