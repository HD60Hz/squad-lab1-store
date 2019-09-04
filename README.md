LAB3 SQUAD TRAINING - PYTHON
===

## Storify
Management store
### 1- Model Store
We will create a store using three data structure, Dictionary, list and tuple  
The dictionary will contain three keys:
* name => name of the store, containing a string value
* inventory => a list of product in tuple:
    - The product tuple will have the name(string), the price(float) and the quantity(integer)
* items_count => an integer containing the total number of products

Now, we have the data structure for our store, it would be good to create a factory function to create our store, our function will have 2 parameters, a name to our store, and inventory to have default products, and it'll return the store  

**Let's see the code**
```python
# our store
store = {
    "name": "",
    "inventory": [("name1", "price", "quantity"), (...), ...],
    "items_count": 0 #total numbers of items, 0 by default
}

# Our factory function to create the store
def create_store(name, inventory=[("screen", 600.0, 3),
                                  ("mouse", 40, 10)]):
    products = []
    items_count = 0
    for product in inventory:
        items_count += product[2]
        products.append(product)

    return {
        "name": name,
        "inventory": products,
        "items_count": items_count
    }


if __name__ == "__main__":
    store = create_store(name="my_store")
```

Now , we can interact with our store

### 2- Interact with the store

In the first section, we create our data structure and the factory function to create our store  
We can now create a repl system to interact with our store
For that, we will use:
* loop
* input
* command system => a dictionary with id, name and handlers  

**Example**
```python
def function1():
    print("test")


def function2():
    print("test2")


list_command = [
    {"id": 1, "name": "name1", "handler": function1},
    {"id": 2, "name": "name2", "handler": function2},
]

def get_command(choice):
    selected_command = None
    if choice == 1:
        selected_command = next((item for item in list_command if item["id"] == choice), None)

    if choice == 2:
        selected_command = next((item for item in list_command if item["id"] == choice), None)

    return selected_command


def start_store_repl(store):
    print("#########-Storify-#########")
    start_store = True
    while start_store:
        print("\tcommand list")
        for command in list_command:
            print("\t", command["id"], " - ", command["name"], sep=" ")

        try:
            choice = int(input("your choice>"))

            command = get_command(choice)
            if command:
                command["handler"]()
            else:
                print("You must choose between [1, 2]")

            start_store = False

        except ValueError:
            print("You must choose an integer")
```

**Let's modify our code**

### 3- Handlers

* We modify function **create_store()** to get name from input 
* We create function **list_inventory()** to list the inventory of the store
* We create function **add_product()** to add product to the store
* We create function **fill_product()** to get product info from input
* We create function **get_command()** to get the selected command from input
* We create function **start_store_repl()** to create the loop on the store
```python
def create_store():
    print("==================================")
    print("==================================")
    print("        Welcome to Storify        ")
    print("==================================")
    print("==================================")
    name = input("Enter a name for the store>")
    inventory = [("screen", 600.0, 3),
                 ("mouse", 40.0, 10)]
    products = []
    items_count = 0
    for product in inventory:
        items_count += product[2]
        products.append(product)

    return {
        "name": name,
        "inventory": products,
        "items_count": items_count
    }


def list_inventory(store):
    while True:
        print(f"######### List inventory of {store['name']} #########")
        inventory = store["inventory"]
        print("#", f"name           ", "price", "quantity", sep="\t\t\t")
        for index, product in enumerate(inventory):
            max_len = 9
            name_len = len(product[0])
            if max_len > name_len:
                name = product[0] + (max_len-name_len) * " "
            else:
                name = product[0][:max_len]
            print(index, name, product[1], product[2], sep="\t\t\t")
        print("Total products:", store["items_count"])

        choice = input("Return to the main menu [y/n]>")
        if choice in ["y", "Y"]:
            break


def add_product(store):
    print("######### Add product to inventory #########")
    while True:
        print("Total products:", store["items_count"])
        print("Do you want to add product ? [y/n]")
        choice = input("your choice>")
        if choice in ["y", "Y"]:
            name, price, quantity = fill_product()

            for index, product in enumerate(store["inventory"]):
                if name.lower() == product[0].lower():
                    edited_product = (name, price, quantity + product[2])
                    store["items_count"] += quantity
                    store["inventory"][index] = edited_product
                    break
            else:
                store["inventory"].append((name, price, quantity))
                store["items_count"] += quantity

        else:
            break


def fill_product():
    name = input("name:")

    while True:
        try:
            price = float(input("price:"))
            break
        except ValueError:
            print("You must enter a number")

    while True:
        try:
            quantity = int(input("quantity:"))
            if quantity <= 0:
                print("The quantity must be > 0")
            else:
                break
        except ValueError:
            print("You must enter an integer")

    return name, price, quantity


list_command = [
    {"id": 1, "name": "list inventory", "handler": list_inventory},
    {"id": 2, "name": "add product to inventory", "handler": add_product},
    {"id": 0, "name": "exit", "handler": False}
]


def get_command(choice):
    selected_command = None
    if choice in [0, 1, 2]:
        selected_command = next((item for item in list_command if item["id"] == choice), None)

    return selected_command


def start_store_repl(store):
    start_store = True
    while start_store:
        print("\tcommand list")
        for command in list_command:
            print("\t", command["id"], " - ", command["name"], sep=" ")

        try:
            choice = int(input("your choice>"))

            command = get_command(choice)
            if command["id"] != 0:
                command["handler"](store)
            elif command["id"] == 0:
                start_store = False
            else:
                print("You must choose between [1, 2]")

        except ValueError:
            print("You must choose an integer")


if __name__ == "__main__":
    store = create_store()
    start_store_repl(store)
```
