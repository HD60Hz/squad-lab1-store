from store import create_store, create_inventory_product, get_store, Product


def start_inventory_creation(store):
    while True:
        print(f"You have {len(store.get('inventory'))} products in your inventory")
        print("1- Add new product", "0- Return to store", sep="\n", end="\n")
        choice = input("")

        if choice == "0":
            break

        name = input("-name: ")
        price = float(input("-price: "))
        quantity = int(input("-quantity: "))

        store.get("inventory").append(
            create_inventory_product(name, price, quantity)
        )


def start_store():
    store = get_store()
    if not store["name"]:
        name = input("Give the name of the store: ")
        store = create_store(name)
    print(f"Welcome to {store['name']}")

    while True:
        print("What do you want to do ?", "1- Update inventory", "0- Exit", sep="\n", end="\n")
        choice = input("")

        if choice == "0":
            break

        if choice == "1":
            start_inventory_creation(store)

    print(store)


def get_product(store, cart):
    while True:
        print(f"You have {len(cart)} products in your cart")
        products = [(i, product) for i, product in enumerate(store.get("inventory"))]
        products = dict(products)

        print("id", "name", "price", "quantity", sep=" " * 10, end="\n")
        for i, product in products.items():
            print(f"{i}", f"{product.name}", f"{product.price}", f"{product.quantity}", sep=" " * 10, end="\n")

        print("Enter the id of the product you want", "tap -1 to exit", sep="\n", end="\n")

        choice = input()

        if choice == "-1":
            break

        choice = int(choice)
        if choice not in products.keys():
            print("Wrong id")
            continue
        else:
            selected_product = products[choice]
            print(f"you selected {selected_product.name}")
            quantity = int(input("Enter quantity: "))

            while quantity > selected_product.quantity:
                quantity = int(input(f"Only {selected_product.quantity} are available, enter quantity: "))

            if products[choice].quantity - quantity <= 0:
                del store.get("inventory")[choice]
            else:
                store.get("inventory")[choice] = Product(products[choice].name,
                                                         products[choice].price,
                                                         products[choice].quantity - quantity)

            cart.append(Product(products[choice].name, products[choice].price, quantity))


def show_cart(cart):
    while True:
        print(cart)
        choice = input("Tap 0 to return: ")

        if choice == "0":
            break


def access_store():
    store = get_store()
    cart = []
    while True:
        if store.get("name"):
            print(f"You are in {store.get('name')}")
            print("What do you want to do ?", "1- Get product", "2- Show my cart", "0- Exit", sep="\n", end="\n")

            choice = input()
            if choice == "0":
                break

            if choice == "1":
                get_product(store, cart)

            if choice == "2":
                show_cart(cart)
        else:
            print("No store available")
            break


def user_type():
    print("Welcome to store managing")

    while True:
        print("Enter as:", "1- Owner", "2- Customer", "0- Exit", sep="\n", end="\n")
        choice = input()

        if choice == "0":
            break

        if choice == "1":
            start_store()

        if choice == "2":
            access_store()


if __name__ == '__main__':
    user_type()
