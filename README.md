LAB1 SQUAD TRAINING - PYTHON
---

### Concurrency
All the execution parts of the application are sequential. When a code take longer to execute, because of long processing or some IO related stuff, the rest of the app need to wait until the end, even though it does not depend on it  
To have a closer look at that, we will try to add a sleep in the ``retrieve_articles`` of the scraper for each article (ex: sleep for 4 seconds)

```python
import time
...
    def retrieve_articles(self) -> Iterable[tuple]:
        response = requests.get(self.__category.value)
        soup = BeautifulSoup(response.content, 'html.parser')

        tiles = soup.select('.article-tile')
        
        articles = []
        for tile in tiles[:10]:
            name = str(tile.select_one('.article-tile__name').next)
            raw_price = str(tile.select_one('.article__price').next)
            price = float(next(re.finditer(r'\d*,\d{2}', raw_price))[0].replace(',', '.'))
            quantity = random.randint(0, 50)

            time.sleep(4)

            articles.append((name, price, quantity))
        
        return articles
...
```

If we remove the inventory database to trigger the scraping then run storify, we will notice a big freeze. It is because the REPL is not yet looping. In fact, the scraping starts when the store initializes. So everything is blocked waiting for the retrieval of all Home24 articles

An analogy to this situation would be:  
Imagine we have a store with an inventory room and a backdoor where our provider can park his truck
* Actually, we work alone. So we need to unload the products and store them in the inventory room. Then, and only then we can open our store and start selling ... sucks doesnt it ?!  
* Imagine we have a super slow computer to manage our store. So we start working on the computer and every time it freezes for a couple of minutes, we cease the occasion to go and unload a couple of products to the inventory then come back. **THAT IS MULTITASKING**
* Now Imagine that we hire an employee to do the work of unloading for us. We can start selling products while the employee is working. Of course the inventory will be empty in the beginning and get filled little by little but it wont block us. **THAT IS PARALLELISM**

**Concurrency** is a broader term that englobes both multitasking and parallelism

In Python to achieve multitasking, we can either use:
* _Thread_ for preemptive multitasking (Limited by the [GIL](https://wiki.python.org/moin/GlobalInterpreterLock) in the case of CPython)
* _Asynchronous IO_ (ex: using [asyncio](https://docs.python.org/3/library/asyncio.html)) for cooperative multitasking

On the other hand to achieve real parallelism, we have to use ``multiprocessing``  
[Here](https://realpython.com/python-concurrency/) is a good introduction all those concepts

Let's improve our application using multitasking, show an example with multiprocessing then finish the chapter with some scheduling to save our inventory to the database

#### Adaptation
To prepare a little bit our existing code, we will change the return type of ``retrieve_articles`` from list to generator (Both iterables so it wont be a problem)

```python
...
    def retrieve_articles(self) -> Iterable[tuple]:
        response = requests.get(self.__category.value)
        soup = BeautifulSoup(response.content, 'html.parser')

        tiles = soup.select('.article-tile')

        for tile in tiles[:10]:
            name = str(tile.select_one('.article-tile__name').next)
            raw_price = str(tile.select_one('.article__price').next)
            price = float(next(re.finditer(r'\d*,\d{2}', raw_price))[0].replace(',', '.'))
            quantity = random.randint(0, 50)

            time.sleep(4)

            yield name, price, quantity
```

Next, in the store initialization, we will encapsulate the code related to scraping and saving to inventory database

```python
...
class Store:
    def __init__(self, name: str):
        self.name = name
        self.__inventory = []
        self.__items_count = 0

        from storify.db.inventory import InventoryFileDB, Types
        self.__inventory_db = InventoryFileDB(Types.CSV)

        db_data = self.__inventory_db.load_products()
        if db_data:
            for product in db_data:
                self.add_product(*product)
        else:
            def push_from_home24(store: Store):
                articles = Home24Scraper().retrieve_articles()
                for article in articles:
                    store.add_product(*article)

                store.save_inventory()

            push_from_home24(self)
```
Now the action of pushing to the inventory uses the store api   
Most importantly, ``push_from_home24`` is decoupled from the rest of the initialization and it expects a store as argument. When there is no data in our base, we fall back to it

All this will help us on the introduction of Thread next

#### Thread
The use of a [Thread](https://docs.python.org/3/library/threading.html) is straight forward: Instantiate one and start it with a target and its arguments. In our case it is ``push_to_home24``

```python
...
class Store:
    def __init__(self, name: str):
        self.name = name
        self.__inventory = []
        self.__items_count = 0

        from storify.db.inventory import InventoryFileDB, Types
        self.__inventory_db = InventoryFileDB(Types.CSV)

        db_data = self.__inventory_db.load_products()
        if db_data:
            for product in db_data:
                self.add_product(*product)
        else:
            def push_from_home24(store: Store):
                articles = Home24Scraper().retrieve_articles()
                for article in articles:
                    store.add_product(*article)

                store.save_inventory()

            task = Thread(target=push_from_home24, args=(self,))
            task.start()
```

Let's test it. Remove the inventory database and run storify

YAY!! No freeze  
Go ahead and run list_inventory multiple times

Result:
<pre>
Welcome to OPEN Store store. Type help or ? to list commands.

Store>list_inventory

Store>list_inventory

Store>list_inventory

Store>list_inventory
    name                  price    quantity
--  ------------------  -------  ----------
 0  Lit boxspring Kinx   879.99           3
Store>list_inventory
    name                  price    quantity
--  ------------------  -------  ----------
 0  Lit boxspring Kinx   879.99           3
Store>list_inventory
    name                  price    quantity
--  ------------------  -------  ----------
 0  Lit boxspring Kinx   879.99           3
Store>list_inventory
    name                  price    quantity
--  ------------------  -------  ----------
 0  Lit boxspring Kinx   879.99           3
Store>list_inventory
    name                         price    quantity
--  -------------------------  -------  ----------
 0  Lit boxspring Kinx          879.99           3
 1  Canapé convertible Latina   399.99          49
Store>
...
</pre>

As you can see the inventory is filling up without blocking our management of the store throught the REPL

Let's step up our game and scrap multiple pages of Home24. We will add **Garden** and **Light** categories pages  
First we will define a ``Home24Categories`` Enum with the targeted URLs

```python
from enum import Enum
...
class Home24Categories(Enum):
    MEUBLE = 'https://www.home24.fr/categorie/meubles/'
    JARDIN = 'https://www.home24.fr/categorie/jardin/'
    LUMINAIRE = 'https://www.home24.fr/categorie/luminaires/'

class Home24Scraper:
    def __init__(self, category: Home24Categories):
        self.__category = category
...
```

Now we can call 1 thread for each categorie and start them

```python
    ...
    if not db_data:
        task_meuble = Thread(target=push_from_home24, args=(self, Home24Categories.MEUBLE))
        task_jardin = Thread(target=push_from_home24, args=(self, Home24Categories.JARDIN))
        task_luminaire = Thread(target=push_from_home24, args=(self, Home24Categories.LUMINAIRE))
        task_meuble.start()
        task_jardin.start()
        task_luminaire.start()
...
```

Great, we are overlapping the task (multitasking) so that when one task is sleeping (4 sec) an other task is run

Now imagine we have 1000 website to scrap. It would be somewhat costly and inefficient to create a Thread for each task. We have to create a **Pool** of threads

``ThreadPoolExecutor`` is a sweet wrapper that hides the complexity of managing multiple Thread. It is offered by the standard module ``concurrent.futures``

```python
from concurrent.futures.thread import ThreadPoolExecutor
...
    ...
    if not db_data:
        executor = ThreadPoolExecutor(max_workers=3)
        executor.submit(push_from_home24, self, Home24Categories.MEUBLE)
        executor.submit(push_from_home24, self, Home24Categories.JARDIN)
        executor.submit(push_from_home24, self, Home24Categories.LUMINAIRE)
...
```

In this example we create 3 worker to handle 3 tasks. But it does not have to be the case. In real world application you need to benchmark you application to find the sweet spot between the number of thread and the task in hand

In functional style it would be...

```python
from functools import partial
...
    ...
    if not db_data:
        executor = ThreadPoolExecutor(max_workers=3)
        executor.map(partial(push_from_home24, self), Home24Categories)
    ...
```

Unlike processes that have their own memory space, threads share their parent process memory. This means that you have to be extra careful about Thread-safety  
If some tasks involve manipulating/referencing the same data, you have to use some mechanism (Locks, conditions...) to make your code thread-safe

In our case the ``items_count`` is incremented by the product quantity. So we can have a race condition if there is a preemptive interruption from the os  
Let's use a ``Lock``

```python
from threading import Lock
    ...
    def push_from_home24(store: Store, lock: Lock, category: Home24Categories):
        articles = Home24Scraper(category).retrieve_articles()
        for article in articles:
            with lock:
                store.add_product(*article)

        with lock:
            store.save_inventory()

    if not db_data:
        l = Lock()`
        executor = ThreadPoolExecutor(max_workers=3)
        executor.map(partial(push_from_home24, self, l), Home24Categories)
...
```

#### Process
[Multiprocessing](https://docs.python.org/3/library/multiprocessing.html) in Python have the same API as threading (seen above). But because each process has its own memory space, it is more complex to manage shared data in our program. The solution must involve some kind of inter-process communication (IPC)  
In our case, because of the shared ``inventory`` and ``items_count``, it would be difficult to find AS a simple and elegant solution AS using threads

This is how it would look like if we want to force the use of a pool of processes and a ``Manager``

```python
from concurrent.futures.process import ProcessPoolExecutor
from functools import partial
from multiprocessing import Manager
from multiprocessing.managers import BaseManager, NamespaceProxy
...
from storify.scraper import Home24Scraper, Home24Categories
from storify.store import Store, push_from_home24

class StoreManager(BaseManager): pass

class StoreProxy(NamespaceProxy):
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__', 'inventory', 'add_product', 'save_inventory')

    def add_product(self, name, price, quantity):
        callmethod = object.__getattribute__(self, '_callmethod')
        return callmethod('add_product', [name, price, quantity])

    def save_inventory(self):
        callmethod = object.__getattribute__(self, '_callmethod')
        return callmethod('save_inventory')

def create_managed_store(name) -> Store:
    manager = StoreManager()
    manager.register("Store", Store, StoreProxy)
    manager.start()

    return manager.Store(name)

def fill_store(s: Store):
    lck = Manager().Lock()
    executor = ProcessPoolExecutor(max_workers=3)
    executor.map(partial(push_from_home24, s, lck), Home24Categories)


def main():
    store = create_managed_store(name="OPEN Store")
    if len(store.inventory) == 0:
        fill_store(store)

    StoreREPL(store).cmdloop()
```

#### Scheduler
Imagine we want to schedule some task to be executed periodically or at a certain time. For example, we need to schedule an event for saving the store inventory every 10 seconds  

There are many libraries in Python to handle scheduling
* [sched](https://docs.python.org/3/library/sched.html) is a simple standard library that offers basic scheduling functionality 
* [schedule](https://github.com/dbader/schedule) is a third-party library alternative with a fluent API (DSL)
* [APScheduler](https://apscheduler.readthedocs.io/en/latest/) is a powerful and complete third-party library with support for concurrency and job storages

First, let's try writing our own implementation with a simple loop and a ``time.sleep``. To avoid blocking we will use a thread

```python
from threading import Thread
import time
...
class Store:
    def __init__(self, name: str):
        self.name = name
        self.__inventory = []
        self.__items_count = 0
        self.__autosave = False
        ...
        ...
        self._register_autosave()

    def _register_autosave(self):
        self.__autosave = True
        class SchedulerSaveThread(Thread):
            @classmethod
            def run(cls):
                while self.__autosave:
                    time.sleep(10)
                    self.save_inventory()

        SchedulerSaveThread().start()

    def close(self):
        self.__autosave = False
```

To allow our program to finish we have to stop the Thread from the inside. In this case by setting ``autosave`` to False  

```python
...
def main():
    store = Store(name="OPEN store")
    StoreREPL(store).cmdloop()
    store.close()
```

Now run storify and keep an eye on the inventory file ... For certainty, add a ``print`` inside ``save_inventory``  
YEP! It is executing the save every 10 seconds without blocking us

Let's try ``apscheduler`` this time. Begin by installing it

```shell script
pip install apscheduler
```

```python
from apscheduler.schedulers.background import BackgroundScheduler
...
    def _register_autosave(self):
        self.__scheduler = BackgroundScheduler()
        self.__scheduler.add_job(self.save_inventory, 'interval', seconds=10)
        self.__scheduler.start()

    def close(self):
        self.__scheduler.shutdown()
```

As simple as that !

We added _APScheduler_ to our dependencies, don't forget to add it to ``requirements.txt``  

```shell script
pip freeze > requirements.txt
```

