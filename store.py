# We Create store as dictionary
# We will use store to save all product tuple
store = {}

# We create product as list of tuple, it contains the default product
# each tuple will create with the form (name_of_product, price_of_product, quantity)
product = [
    ("keyboard", 10.0, "10"),
    ("mouse", 10.0, "3"),
    ("desktop", 450.0, "5")
]

#
for i in range(3):
    store[i] = product[i]


# We use a loop to add product
def add_product():
    """Add product to the store"""
    while True:
        print("What do you want to do?", "\t1- Add new product", "\t0- Exit", sep="\n", end="\n")
        choice = input("Your choice>")
        if choice == "0":
            list_product()
            break
        if choice == "1":
            print("Add a new product")
            name = input("> name: ")
            price = input("> price: ")
            quantity = input("> quantity: ")
            product = (name, price, quantity)
            index = len(store.keys())
            store[index] = product


def list_product():
    """List all product from the store"""
    print("List of product")
    print("#", "name", "price", "quantity", sep="\t|\t", end="\n")
    for index, product in store.items():
        print(index, product[0], product[1], product[2], sep="\t|\t", end="\n")


while True:
    """We use a while loop to interact with the user"""
    print("What do you want to do?", "\t1- Add product", "\t2- List product", "\t0- Exit", sep="\n", end="\n")
    choice = input("Your choice>")
    if choice == "0":
        break
    if choice == "1":
        add_product()
    if choice == "2":
        list_product()

print("Bye")
