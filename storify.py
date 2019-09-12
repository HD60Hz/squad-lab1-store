from collections import namedtuple

from tabulate import tabulate

Product = namedtuple("Product", ["name", "price", "quantity"])
Command = namedtuple("Command", ["id", "name", "handler"])


def create_store(name, inventory=[]):
    items_count = 0
    for product in inventory:
        items_count += product.quantity

    return {
        "name": name,
        "inventory": inventory,
        "items_count": items_count
    }


def list_inventory(store):
    print(tabulate(store["inventory"], headers="keys", showindex=True))


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


COMMANDS = [
    Command(0, "Exit", lambda _: exec('raise StopIteration')),
    Command(1, "List inventory", list_inventory),
    Command(2, "Add product", add_product),
    Command(3, "Remove product", remove_product),
    Command(4, "Modify product", modify_product),
]


def print_commands():
    for command in COMMANDS:
        print("\t", command.id, " - ", command.name, sep=" ")


def get_handler(cmd_id):
    return next((command.handler for command in COMMANDS if command.id == cmd_id), None)


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
        except StopIteration:
            print("Bye !")
            break


if __name__ == "__main__":
    store = create_store(
        name="OPEN Store",
        inventory=[
            Product("screen", 600.0, 3),
            Product("mouse", 40, 10)
        ]
    )
    run_store_shell(store)
