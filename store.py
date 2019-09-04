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
            # name = input("name:")
            # price = float(input("price:"))
            # quantity = int(input("quantity:"))
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

