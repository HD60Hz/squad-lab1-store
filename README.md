LAB3 SQUAD TRAINING - PYTHON
---

We will create an app store named Storify
* Specifications
    - List product
    - add product

## Storify
### Create dictionary and tuple
We will use a list of tuple to get default product and a dictionary to save all products
```python
store =  {}
product = [
    ("keyboard", 10.0, "10"),
    ("mouse", 10.0, "3"),
    ("desktop", 450.0, "5")
]
```
You can print the product variable to see the result
```python
print(product)
```
Run store.py:
```shell
python store.py
```
Result:
> \[('keyboard', 10.0, '10'), ('mouse', 10.0, '3'), ('desktop', 450.0, '5')\]

To save all product in our dictionary, we'll use a for loop with range Because we know the number of product 
```python
for i in range(3):
    store[i] = product[i]
```
You can print the store variable to see the result
```python
print(store)
```
Run store.py:
```shell
python store.py
```
Result:
> {0: ('keyboard', 10.0, '10'), 1: ('mouse', 10.0, '3'), 2: ('desktop', 450.0, '5')}
### Create function list_product and add_product
We will create a function list product to list all product in a table
```python
def list_product():
    """List all product from the store"""
    print("List of product")
    print("#", "name", "price", "quantity", sep="\t|\t", end="\n")
    for index, product in store.items():
        print(index, product[0], product[1], product[2], sep="\t|\t", end="\n")
```
We use the second print to display the header of the table  
* The **sep** parameter is the separator between the arguments of string (default is space " ")
    - We use "\t|\t" which is **tabulation** + | + **tabulation**
* The **end** parameter is end of the print (default is **\n** new line)

We use the for loop to iterate through the store dictionary  
* **store.items()** return a list containing the tuple with the **key** and the **value**

And, we launch the print to display each product of the store dictionary
* **index** is the key 
* **product** is the value (tuple) => product\[0] is the name, product\[1] is the price and product\[2] is the quantity

We can call our function
```python
list_product()
```
Run store.py:
```shell
python store.py
```
Result:
> List of product  
> \#      |       name    |       price   |       quantity  
> 0       |       keyboard        |       10.0    |       10  
> 1       |       mouse   |       10.0    |       3  
> 2       |       desktop |       450.0   |       5

We will create a function add product to add a new product to the store
```python
def add_product():
    """Add product to the store"""
    print("Add a new product")
    name = input("> name: ")
    price = input("> price: ")
    quantity = input("> quantity: ")
    product = (name, price, quantity)
    index = len(store.keys())
    store[index] = product
    list_product()
```
**name**, **price** and **quantity** are **input**
* **input** allows user to enter strings using keyboard

So, we invite user to enter a name, a price and a quantity for new product  
We create a tuple for the new product  

```python
index = len(store.keys())
```
store.keys() return a list of all keys, in our case, it's \[0, 1, 2]  
len(store.keys) return the total numbers of items, it's 3  
So, we can use index to save a new product
```python
store[index] = product
```
We call list_product() to display our new store with the new product

We can call our function
```python
add_product()
```
Run store.py:
```shell
python store.py
```
Result:
> Add a new product  
> \> name: monitor  
> \> price: 600  
> \> quantity: 5  
> List of product  
> \#       |       name    |       price   |       quantity  
> 0       |       keyboard        |       10.0    |       10  
> 1       |       mouse   |       10.0    |       3  
> 2       |       desktop |       450.0   |       5  
> 3       |       monitor |       600     |       5  

AS you can see we have a new product as index with the entered value
> 3       |       monitor |       600     |       5

### Implement a basic REPL (Read–eval–print loop)

We will add a While loop to interact with the user
```python
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
```
* First, we use a print to indicate the user the different choice available
* Next, we save the choice of the user in choice variable, using input
* Depending of the choice of the user, we run  different actions:
    - "O" => **break** we interrupt the loop to quit 
    - "1" => We run **add_product()** to add a new product
    - "2" => We run **list_product()** to list all the product
* We add the last print out of the loop when we choose "0"

Let's try:
Run store.py:
```shell
python store.py
```
Result:
> What do you want to do?  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1- Add product  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2- List product  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0- Exit  
> Your choice>1
> Add a new product  
> \>name: screen  
> \>price: 600  
> \>quantity: 3  
> List of product  
> \#       |       name    |       price   |       quantity  
> 0       |       keyboard        |       10.0    |       10  
> 1       |       mouse   |       10.0    |       3  
> 2       |       desktop |       450.0   |       5  
> 3       |       screen  |       600     |       3  
> What do you want to do?  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1- Add product  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2- List product  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0- Exit  
> Your choice>0  
> Bye

As you can see, we added a new product, we have a display the list of product and we return to the choice **What do you want to do?**  
We choose "0" to quit and we have the message **Bye**

#### Update function with loop
We will now update our functions add_product to add several product at once
```python
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
```
* First, we use a print to indicate the user the different choice available
* Next, we save the choice of the user in choice variable, using input
* Depending of the choice of the user, we run  different actions:
    - "O" => **break** we interrupt the loop to quit, but before quit, we display the list of product
    - "1" => We add the product with name, price and quantity

When the loop is broke, we return to the main loop of the script

Run store.py:
```shell
python store.py
```
Result:
> What do you want to do?  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1- Add product  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2- List product  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0- Exit  
> Your choice>1  
> What do you want to do?  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1- Add new product  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0- Exit  
> Your choice>1
> Add a new product  
> \>name: screen  
> \>price: 600  
> \>quantity: 3  
> What do you want to do?  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1- Add new product  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0- Exit  
> Your choice>1  
> \>name: desktop  
> \>price: 1000
> \>quantity: 1  
> What do you want to do?  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1- Add new product  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0- Exit  
> Your choice>0  
> List of product  
> \#       |       name    |       price   |       quantity  
> 0       |       keyboard        |       10.0    |       10  
> 1       |       mouse   |       10.0    |       3  
> 2       |       desktop |       450.0   |       5  
> 3       |       screen  |       300     |       2  
> 4       |       desktop |       1000    |       1  
> What do you want to do?  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1- Add product  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2- List product  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0- Exit  
> Your choice>0  
> Bye

As you can see, when you choose add product from the main loop, We have a second loop which ask Add a new product or exit. When you add a new product, we have the same loop which ask again to Add a new product or exit
