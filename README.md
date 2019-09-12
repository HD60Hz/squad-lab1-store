LAB1 SQUAD TRAINING - PYTHON
---

### Storify
For the rest of this lab we are going to focus on the creation of a store management application. This will allow us to have a practical context for our Python learning.
First we need to define some simple use case specifications that will bound our application and that we can extend later if we want to.

#### Specifications
* As a manager,
	* I can list the inventory (id, name, price and products quantity).
	* I can add a product to the inventory by providing a name, price and quantity
	* I can remove a product from the inventory by id
	* I can modify a product from the inventory by id

#### Model
Now we need to model our store before we can interact with it. To do so, we are going to use three data structure : Dictionary, List and Tuple.

The store will be represented by a dictionary of 3 values :
* name : a string value representing the name of the store
* inventory : a list of products
* items_count : an integer containing the total number of products in the store

The products will be represented by a tuple of 3 values :
1. a string value representing the name
2. a float value representing the price
3. an integer value representing the quantity

```python
store = {
    "name": "",
    "inventory": [("name1", "price1", "quantity1"), (...), ...],
    "items_count": 0 #total numbers of items, 0 by default
}
```

It would be good to create our store using a factory function that will encapsulate our model. This function will receive 2 arguments : a name for the store, and an initial inventory (optional).

```python
# product mapping
P_NAME, P_PRICE, P_QUANTITY = range(3)

def create_store(name, inventory=[]):
    items_count = 0
    for product in inventory:
        items_count += product[P_QUANTITY]

    return {
        "name": name,
        "inventory": inventory,
        "items_count": items_count
    }


if __name__ == "__main__":
    store = create_store(
			    name="my_store",
				inventory=[("screen", 600.0, 3), ("mouse", 40, 10)]
			)

	print(store)
```
To avoid pointing to product attributes by index in the tuple, we can replace it with a nametuple. It is a subclass used to create tuple-like objects that have fields accessible by attribute lookup as well as being indexable and iterable.

```python
from collections import namedtuple

Product = namedtuple("Product", ["name", "price", "quantity"])

def create_store(name, inventory=[]):
    items_count = 0
    for product in inventory:
        items_count += product.quantity

    return {
        "name": name,
        "inventory": inventory,
        "items_count": items_count
    }


if __name__ == "__main__":
    store = create_store(
			    name="my_store",
				inventory=[
					Product("screen", 600.0, 3),
					Product("mouse", 40, 10)
				]
			)

	print(store)
```

We are ready to implement our use cases... or are we ?!!

#### REPL
We need an interface to allow the manager to interact with his store (Shell, GUI, Web API...). We will stick with the common shell interface (for now) and we are going to use a [REPL](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop) (read–eval–print–loop) system.

##### Exercice
Create a simplistic REPL using only an infinite loop, input/print functions and a command/handler pattern.

##### Solution
```python
Command = namedtuple("Command", ["id", "name", "handler"])

def handler1():
    print("Handling command 1...")

def handler2():
    print("Handling command 2...")

COMMANDS = [
	Commande(1, "Command 1", handler1),
	Commande(2, "Command 2", handler2)
]

def print_commands():
    for command in COMMANDS:
        print("\t", command.id, " - ", command.name, sep=" ")

def get_handler(cmd_id):
    return next((command.handler for command in COMMANDS if command.id == cmd_id), None)

def run_shell():
    while True:
        print_commands()

        try:
            cmd_id = int(input("your choice> "))

            handler = get_handler(cmd_id)
            if not handler:
                print("You must choose a valid command")
                continue

			handler()

        except ValueError:
            print("You must provide a command id")

if __name__ == "__main__":
    run_shell()
```

#### Use cases
  Based on the example above lets create a REPL version for our store, then start implementing the use cases defined in the beginning of the chapter
```python
...
def create_store(name, inventory=[]):
   ...

def list_inventory(store):
    print("Handling...")

def add_product(store):
    print("Handling...")

def remove_product(store):
    print("Handling...")

def modify_product(store):
    print("Handling...")

COMMANDS = [
    Command(1, "List inventory", list_inventory),
	Command(2, "Add product", add_product),
	Command(3, "Remove product", remove_product),
	Command(4, "Modify product", modify_product),
]

def print_commands():
	...

def get_handler(cmd_id):
	...

def run_store_shell(store):
    print("=" * 34)
    print("{:^34}".format(f"Welcome in {store['name']}"))
    while True:
       print("=" * 34)
	   print("{:^34}".format(f"Items count : {store['items_count']} \n"))
	   print_commands()

        try:
            cmd_id = int(input("your choice> "))

            handler = get_handler(cmd_id)
            if not handler:
                print("You must choose a valid command")
                continue

			print("=" * 34)
            handler(store)

        except ValueError:
            print("You must provide a command id")


if __name__ == '__main__':
    store = create_store('OPEN Store')
    run_store_shell(store)
```

You can notice that, with this version, each command handler receive a context (store) as argument. This will allow them to update the mutable context to achive their purpose.

When we run the program
```shell
python storify.py
```
Result :
<pre>

=================================
      Welcome in OPEN Store
==================================
        Items count : 13

	 1  -  List inventory
	 2  -  Add product
	 3  -  Remove product
	 4  -  Modify product
your choice>

</pre>

We will suppose that product identifier is exactly the product index in the inventory list. Again, for the sake of simplicity.

* **List inventory**
```python
...
def list_inventory(store):
    inventory = store["inventory"]
    name_cell, price_cell, quantity_cell = "{:<10}", "{:>6}", "{:>6}"
	for i, product in enumerate(inventory):
        print(i,
			  name_cell.format(product.name),
			  price_cell.format(product.price),
			  quantity_cell.format(product.quantity))
...
if __name__ == '__main__':
    store = create_store('OPEN Store', [
				Product("screen", 600.0, 3),
				Product("mouse", 40, 10)
			])
    run_store_shell(store)
```
When we choose the command 1 corresponding to inventory listing we get :

<pre>
0 screen      600.0      3
1 mouse          40     10
</pre>

A better way to print a list in tabular form is to use some existing library like ``tabulate``
We begin by installing it using :
```shell
pip install tabulate
```
Next, we need to import it in our code and use it
```python
from tabulate import tabulate
...
def list_inventory(store):
    print(tabulate(store["inventory"], headers="keys", showindex=True))
...
```
Result :
<pre>
    name      price    quantity
--  ------  -------  ----------
 0  screen      600           3
 1  mouse        40          10
</pre>

* **Add product**
```python
def add_product(store):
	try:
	    print("Add new product...")
	    name = input("Name> ")
	    price = float(input("Price> "))
	    quantity = int(input("Quantity> "))

	    store['inventory'].append(Product(name, price, quantity))
	    store['items_count'] += quantity

	except ValueError:
	    print("You must provide a valid product")
```
When we choose the command 2 corresponding to adding new  product we get :

<pre>
Add new product...
Name> Chocolat
Price> 40
Quantity> 30
</pre>

Re-listing the inventory will prove that the new product is added

<pre>
    name        price    quantity
--  --------  -------  ----------
 0  screen        600           3
 1  mouse          40          10
 2  Chocolat       40          30
</pre>

* **Remove product**
```python
def remove_product(store):
	try:
	    index = int(input("Choose a product> "))

	    removed = store["inventory"].pop(index)
	    store['items_count'] -= removed.quantity

	    print("Product has been removed : {!r}".format(removed))

	except ValueError:
	    print("You must provide a product id")
	except IndexError:
	    print("You must choose an existing product")
```
When we choose the command 3 corresponding to removing existing product we get :

<pre>
Choose a product> 0
Product has been removed : Product(name='screen', price=600.0, quantity=3)
</pre>

Re-listing the inventory will prove that the chosen product is removed

<pre>
    name      price    quantity
--  ------  -------  ----------
 0  mouse        40          10
</pre>

Notice that the id 0 is still present because the inventory has been reindexed (id = index for simplicity)

* **Modify product**
```python
def modify_product(store):
	try:
	    index = int(input("Choose a product> "))

	    modified = store['inventory'][index]
	    print("Modify product : {!r}".format(modified))
	    name = input(f"Name [{modified.name}]> ") or modified.name
	    price = float(input(f"Price [{modified.price}]> ") or modified.price)
	    quantity = int(input(f"Quantity [{modified.quantity}]> ") or modified.quantity)

	    store['inventory'][index] = Product(name, price, quantity)
	    store['items_count'] += (quantity - modified.quantity)

	except ValueError:
	    print("You must provide a product id")
	except IndexError:
	    print("You must choose an existing product")
```
When we choose the command 4 corresponding to modifing existing product we get :

<pre>
Choose a product> 0
Modify product : Product(name='screen', price=600.0, quantity=3)
Name [screen]> Chocolat
Price [600.0]>
Quantity [3]>
</pre>

Re-listing the inventory will prove that the chosen product has been modified
<pre>
    name        price    quantity
--  --------  -------  ----------
 0  Chocolat      600           3
 1  mouse          40          10
</pre>

* **Exiting**

Even though we did not specify it at the beginning, we need a last use case to allow the manager to exit his store gracefully.
Let's add a command ``Exit``

We implemented the REPL system so that each time a command is chosen the corresponding handler is invoked. We have to add a way for the handler to notify the REPL to stop its infinite loop and allow the program to exit.

One hacky solution (for learning purpose) is to raise an exception to notify from the handler to allow REPL to stop by catching it.

> StopIteration is a builtin exception used to stop iteration over iterators

```python
COMMANDS = [
    Command(0, "Exit", lambda _: exec('raise StopIteration'))
    ...
]
...
def run_store_shell(store):
	while True:
		...
	    try:
	        ...
	        handler(store)
			...
		...
	    except StopIteration:
	        print("Bye !")
	        break
```

When we choose the command 0 to exit we get :

<pre>
        Items count : 13

	 0  -  Exit
	 1  -  List inventory
	 2  -  Add product
	 3  -  Remove product
	 4  -  Modify product
your choice> 0
==================================
Bye !

Process finished with exit code 0
</pre>
