LAB1 SQUAD TRAINING - PYTHON
---

### Customer
A store is meaningless without a customer. We will try to create a shopping simulation from our store

#### Specifications

As a customer,

* I can list the inventory (id, name, price and products quantity).
* I can list my cart
* I can pick a product from the inventory to my cart by id and quantity
* I can drop a product from my cart by id 
* I can checkout

#### Refactoring
Before we start implementing the customer REPL, we need refactor our store to introduce a _product identifier_ to identify product in cart even after inventory modification  
We will create a sequential id system where we keep track of the last id and increment it each time we add a product. While processing database products, we will resolve the max product id as the last id to continue from  

```python
from typing import Dict
...
Product = namedtuple("Product", ["id", "name", "price", "quantity"])
...
class Store:
    def __init__(self, name: str):
        self.name = name
        self.__last_id = 0
        self.__inventory = {}
        self.__items_count = 0
        ...
        db_data = self.__inventory_db.load_products()
        if db_data:
            for product in db_data:
                self._index_in_inventory(product)
        ...
    def _index_in_inventory(self, product: Product):
        self.__inventory[product.id] = product
        self.__items_count += product.quantity
        self.__last_id = max(self.__last_id, product.id)

    def add_product(self, name: str, price: float, quantity: int) -> Product:
        try:
            price = float(price)
            quantity = int(quantity)

        except ValueError:
            raise ValueError(f'Invalid product input: {name}, {price}, {quantity}')

        self.__last_id += 1
        new = Product(self.__last_id, name, price, quantity)
        self._index_in_inventory(new)

        return new

    def remove_product(self, product: Product):
        try:
            del self.__inventory[product.id]

        except KeyError:
            raise ValueError(f'Unknown product: {product!r}')

        self.__items_count -= product.quantity
    ... 
    @property
    def inventory(self) -> Dict[int, Product]:
        return self.__inventory.copy()
```

For the old use case of **modifiying products**, we need to create a special method to update a product because we want to preserve its id

```python
    ...
    def update_product(self, product: Product, name: str, price: float, quantity: int):
        if product.id not in self.__inventory:
            raise ValueError(f'Unknown product: {product!r}')

        try:
            price = float(price)
            quantity = int(quantity)

        except ValueError:
            raise ValueError(f'Invalid product input: {name}, {price}, {quantity}')

        self.__inventory[product.id] = Product(product.id, name, price, quantity)
    ...
```
Now we need to adapt all the code impacted by this change

##### Save inventory
Saving products still needs an iterable. So we provide the ``values`` of our inventory map

```python
    ...
    def save_inventory(self):
        self.__inventory_db.save_products(self.__inventory.values())
    ...
```

##### Loading products from database
Because we save the id in the database (file), we need to recreate the product with the integer id
```python
    ...
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
    ...
```

##### REPL
Instead of identifing the product by index in inventory. We now have a dedicated id. Because we use a ``dict`` and keys are accessible like indices, there is not a lot of change

```python
    ...
    def do_list_inventory(self, args):
        """List inventory"""
        print(tabulate(self.__store.inventory.values(), headers='keys'))
    ...
```

To modify a product, we invoke the ``update_product`` instead of  ``add_product`` then ``remove_product``

```python
    ...
    def do_modify_product(self, args):
        """Modify existing product in inventory"""
        try:
            id = int(input('Choose a product> '))
            modified = self.__store.inventory[id]

        except (KeyError, ValueError):
            print('Error: You must provide an existing product id')
            return

        print(f'Modify product: {modified!r}')
        name = input(f'Name [{modified.name}]> ') or modified.name
        price = input(f'Price [{modified.price}]> ') or modified.price
        quantity = input(f'Quantity [{modified.quantity}]> ') or modified.quantity

        try:
            self.__store.update_product(modified, name, price, quantity)

        except ValueError:
            print('Error: You must provide a valid product')
    ...
```

That's about it! Now we can continue our implementation of customer use cases

### EXERCICE:
From the test describe below and its result, implement all the shopping use cases

Test:
* List inventory
* Pick a product with quantity
* Pick a second product with quantity
* Pick a third product with quantity
* Pick the first picked product with another quantity
* List cart
* Discard the second picked product
* List cart
* Checkout to see the recap
* List inventory to verify the new quantities of the picked products

Result:
<pre>
Welcome to OPEN store store. Type help or ? to list commands.

Store>simulate_customer
Customer>list_inventory
  id  name                                  price    quantity
----  ----------------------------------  -------  ----------
   1  Suspension Brooklyn I                219.99          28
   2  Table de jardin Iwate (extensible)   129.99          11
   3  Lit boxspring Kinx                   879.99          19
   4  Lampadaire Tripod Iver               119.99          41
   5  Paravent Pirot                        89.99          16
   6  Canapé convertible Latina            399.99          33
   7  Suspension Brooklyn II               149.99          49
   8  Parasol Sombrilla III                 84.99          33
   9  Meuble bas Manchester II             599.99          49
  10  Lampadaire Loppa                      89.99          12
  11  Ensemble lounge Paradise Lounge II   779.99          14
  12  Meuble TV Atelier II                 649.99          49
Customer>pick_product
Choose a product> 1
Picking product: Product(id=1, name='Suspension Brooklyn I', price=219.99, quantity=28)
How many? 3
Customer>pick_product
Choose a product> 2
Picking product: Product(id=2, name='Table de jardin Iwate (extensible)', price=129.99, quantity=11)
How many? 1
Customer>pick_product
Choose a product> 5
Picking product: Product(id=5, name='Paravent Pirot', price=89.99, quantity=16)
How many? 2
Customer>pick_product
Choose a product> 1
Picking product: Product(id=1, name='Suspension Brooklyn I', price=219.99, quantity=28)
How many? 3
Customer>list_cart
1 Suspension Brooklyn I 219.99 x 6
2 Table de jardin Iwate (extensible) 129.99 x 1
5 Paravent Pirot 89.99 x 2
Customer>discard_product
Choose a product> 2
Customer>list_cart
1 Suspension Brooklyn I 219.99 x 6
5 Paravent Pirot 89.99 x 2
Customer>checkout
You have purchased:
Suspension Brooklyn I 219.99 x 6
Paravent Pirot 89.99 x 2
Total: 1499.92
Customer>exit
Store>list_inventory
  id  name                                  price    quantity
----  ----------------------------------  -------  ----------
   1  Suspension Brooklyn I                219.99          22
   2  Table de jardin Iwate (extensible)   129.99          11
   3  Lit boxspring Kinx                   879.99          19
   4  Lampadaire Tripod Iver               119.99          41
   5  Paravent Pirot                        89.99          14
   6  Canapé convertible Latina            399.99          33
   7  Suspension Brooklyn II               149.99          49
   8  Parasol Sombrilla III                 84.99          33
   9  Meuble bas Manchester II             599.99          49
  10  Lampadaire Loppa                      89.99          12
  11  Ensemble lounge Paradise Lounge II   779.99          14
  12  Meuble TV Atelier II                 649.99          49
Store>
</pre>

### Solution:

#### Cart
First let's add a cart system. The store need to track the created carts and the checkout cart

```python
from collections import namedtuple, defaultdict
...
class Store:
    def __init__(self, name: str):
        self.name = name
        self.__last_id = 0
        self.__inventory = {}
        self.__items_count = 0
        self.__carts = []
        self.__checked_carts = []
...
class Cart:
    def __init__(self, inventory):
        self.__inventory = inventory
        self.__products = defaultdict(lambda: 0)  # or defaultdict(int)
...
```
The cart stores the picked product as: product id (key) to quantity (value). Using the ``defaultdict`` allows us to have a default quantity (zero) for a new picked product

##### Pick/discard product
A product picked twice have the old and new quantity cumulated

```python
    ...
    def pick_product(self, product, quantity):
        if product.id not in self.__inventory:
            raise ValueError(f'Unknown product: {product!r}')

        try:
            quantity = self.__products[product.id] + int(quantity)
        except ValueError:
            raise ValueError(f'Invalid quantity: {quantity}')

        if not (0 < quantity <= product.quantity):
            raise ValueError(f'Invalid quantity: {quantity}')

        self.__products[product.id] = quantity

    def discard_product(self, product):
        if product.id not in self.__products:
            raise ValueError(f'Unknown product: {product!r}')

        del self.__products[product.id]

    @property
    def content(self) -> Iterable[Tuple[Product, int]]:
        return ((self.__inventory[id], quantity) for id, quantity in self.__products.items())
```
The content of cart return a generator of ``tuple(product, quantity)``

##### Create and checkout carts
The creation of store cart must be done through the store API. We can then track and validate cart at checkout

```python
...
Purchase = namedtuple("Purchase", ["name", "price", "quantity"])

class Store:
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

        return purchases, total
```
All the cart actions are virtual and does not affect the inventory till checkout time. The checkout update inventory products quantities, flags the cart and returns a list of purchases with total

#### Customer REPL
This REPL is quite similar to the store one. It will create a cart from the provided store when instantiated then simply, for each use case, call the new API (above), catch its exceptions and present them accordingly 

```python
class CustomerREPL(Cmd):
    prompt = "<Customer>"

    def __init__(self, store: Store):
        self.__store = store
        self.__cart = self.__store.create_cart()
        super().__init__()

    def do_list_inventory(self, args):
        """List inventory"""
        print(tabulate(self.__store.inventory.values(), headers='keys'))

    def do_list_cart(self, args):
        """List products in cart"""
        for product, quantity in self.__cart.content:
            print(f'{product.id} {product.name} {product.price} x {quantity}')

    def do_pick_product(self, args):
        """Adding inventory product to customer cart"""
        try:
            id = int(input('Choose a product> '))
            picked = self.__store.inventory[id]

        except (KeyError, ValueError):
            print('Error: You must provide an existing product id')
            return

        print(f'Picking product: {picked}')
        quantity = input('How many? ')

        try:
            self.__cart.pick_product(picked, quantity)

        except ValueError:
            print('Error: You must provide a valid quantity')

    def do_discard_product(self, args):
        """Removing inventory product to customer cart"""
        try:
            id = int(input('Choose a product> '))
            discarded = self.__store.inventory[id]
            
        except (KeyError, ValueError):
            print('Error: You must provide an existing product id')
            return
        
        try:
            self.__cart.discard_product(discarded)

        except ValueError:
            print('Error: Product not in cart')

    def do_checkout(self, args):
        """Checkout"""
        try:
            purchases, total = self.__store.checkout(self.__cart)

            print('You have purchased:')
            for purchase in purchases:
                print(f'{purchase.name} {purchase.price} x {purchase.quantity}')

            print(f'Total: {total}')
        except Exception as e:
            print(e)

    def do_exit(self, args):
        """Exit customer session"""
        return True
```
For the checkout, the return purchases and total is displayed as a recap for the customer

We can nest ``Cmd`` objects by starting their loop in the parent command handler

```python
class StoreREPL(Cmd):
    ...
    def do_simulate_customer(self, args):
        CustomerREPL(self.__store).cmdloop()
    ...
```


