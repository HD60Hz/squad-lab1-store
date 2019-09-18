LAB1 SQUAD TRAINING - PYTHON
---

### Scraping
Till now, we have being focusing only on super motivated eager managers that are ready to spend time managing the inventory product by product. There are a lot of LAZY managers out there that have the need to run their store and have an automatically collected inventory from a remote place. This is just a stupid and naive functionality that we will add to introduce : Scraping the web
Web Scraping is simply the action of extracting data from websites. The 'Web' part of the term reference the use of the World Wide Web and generally its popular protocole : HTTP.
Scraping can be done manually by a hard working person but normally it refers to the use of an automated process (bot, web crawler) to retrieve data into some kind of database for futur uses (ex: Data analysis)
Unless we want to create a complex and intelligent scraping (crawler-like) system that will automatically analyse different website structures and dynamically search for the targeted informations, the common way of conceptualizing a scraper involve analysing manually the unique and unchanged structure of a single website then code accordingly

The website that will be used for this lab is **Home24**

#### Home24 structure
Let's open the e-commerce website ``home24.fr`` to the furniture category : [https://www.home24.fr/categorie/meubles/](https://www.home24.fr/categorie/meubles/)
Using our debugging tool, analyse the articles section of the page (html)

```html
...
<div class="acte-list-view-articles-ctn article-list js-article-list" data-options="...">
	<div class="topsellers">...</div>
	<div class="article-list__items row row--with-3-columns">...</div>
</div>
...
```
First we can notice the presence of a ``data-options`` attribute for ``div`` element with all the data related to articles
This data can be retrieved then parsed to extract some products (name, price ...)
We are going to take a different route and try to focus on the article tiles. The article section is composed of 2 subsections : ``topsellers`` and ``acticle_list``

Each of those contain multiple ``article_tile`` sections

```html
...
<div class="article-tile js-article-tile acte-article-wrapper" data-gtm-bind="click,appear"
  data-sku="000000001000008808" data-gtm-binded="true">						   		 		      <div class="article-tile__wrap">
 <div class="article-tile__images">... </div>

 <a href="/article/meuble-tv-atelier-ii-acacia-partiellement-massif-lava-979486"
  class="article-tile__link js-article-tile__link acte-article-catalogName-lnk">
  Meuble TV Atelier II </a>

 <div class="article-tile__name">Meuble TV Atelier II</div>

 <div class="article__price-wrap ">
 <span class="article__price "> 649,99 €    </span>
 </div>
 <div class="article-tile__rating">...</div>
  ...
    </div>

 <div class="article-tile__related">...</div>
</div>
...
```
We need to extract just 2 informations for each article :
* Product name present in the ``article-tile__name`` div element
* Product price present in the ``article__price`` div element

#### HTTP request Tool
* [urllib](https://docs.python.org/3.1/library/urllib.request.html#module-urllib.request) is a module built into the Python standard library and uses [http.client](https://docs.python.org/3.1/library/http.client.html) which implements the client side of HTTP and HTTPS protocols.

* [urllib3](https://urllib3.readthedocs.io/en/latest/) is a powerful, _sanity-friendly_, third-party HTTP client library. urllib3 brings many critical features that are missing from the Python standard libraries :
	*	Thread safety.
	*	Connection pooling.
	*	Client-side SSL/TLS verification.
	*	File uploads with multipart encoding.
	*	Helpers for retrying requests and dealing with HTTP redirects.
	*	Support for gzip and deflate encoding.
	*	Proxy support for HTTP and SOCKS.
* [requests](https://2.python-requests.org/en/master/) is an elegant and simple HTTP library for Python built on top of urllib3. It is highly recommanded library inside the Python community. This wrapper offers a super easy to use API and extended functionalities compared to the previous libs :
	*  International Domains and URLs
	*	Sessions with Cookie Persistence
	*	Browser-style SSL Verification
	*	Elegant Key/Value Cookies
	*	Automatic Decompression
	*	Unicode Response Bodies
	*	Streaming Uploads and Multiple Multipart Files Uploads
	...

Obviously we are going to use the ``requests`` library.
Because it is not a standard one, we have to install it. From our virtual environement, run the command :

```shell
pip install requests
```
Result:

> Successfully installed certifi-2019.9.11 chardet-3.0.4 idna-2.8 requests-2.22.0 urllib3-1.25.3

### Home24 Scraper
Let's create a ``scraper`` module along side the ``store`` module
<pre>
.
├── ...
├── scraper.py
└── store.py
</pre>

We then need to define the ``Home24Scraper``

```python
import requests

class Home24Scraper:
    url_target = 'https://www.home24.fr/categorie/meubles/'

  def retrieve_articles(self):
        response = requests.get(self.url_target)
	    return response.content

if __name__ == '__main__':
   print(Home24Scraper().retrieve_articles())
```

Let's run the module to see what we get as result. Run command

```shell
python storify/scraper.py
```
OH!! We get all the html page content as bytes. it is not exploitabled as is. We need to parse it

#### Beautiful Soup 4
[BS4](http://www.crummy.com/software/BeautifulSoup/) is a Python library for parsing and pulling data out of HTML and XML files. It provides ways to navigate, search, and modify the parse tree (soup)

We will create a soup out of the response content, then search for the article tiles and finish by extracting names and prices

Don't forget to install ``bs4`` first. Run command

```shell
pip install bs4
```
Result:
> Successfully installed beautifulsoup4-4.8.0 bs4-0.0.1 soupsieve-1.9.3

Our store need product quantities. But the Home24 website does not display them for their articles. We will generate fake and random quantities for each instance. Our LAZY managers won't notice any way

10 articles is enough

```python
def retrieve_articles(self) -> Iterable[tuple]:
    response = requests.get(self.url_target)
    soup = BeautifulSoup(response.content, 'html.parser')

    tiles = soup.select('.article-tile')

    articles = []
    for tile in tiles[:10]:
        name = str(tile.select_one('.article-tile__name').next)
        raw_price = str(tile.select_one('.article__price').next)
        price = float(next(re.finditer(r'\d*,\d{2}', raw_price))[0].replace(',', '.'))
        quantity = random.randint(0, 50)

        articles.append((name, price, quantity))

    return articles
```
The displayed price for the articles have a special format : <pre>'     300,00   '</pre> that can not be parsed/casted with ``float()``. To solve that we use the builtin regular expression library ``re`` in order to retrieve the price using a pattern (Integer + decimal parts rejoined with ``.`` seperator)

Let's check what we retrieved now. Run command

```shell
python storify/scraper.py
```
Result :

> [('Matelas confort Premium Smood', 299.99, 21), ('Lit boxspring Kinx', 879.99, 4), ('Canapé convertible Latina', 399.99, 17), ('Meuble TV Atelier II', 649.99, 14), ('Meuble bas Manchester I', 449.99, 9), ('Meuble bas Manchester II', 599.99, 21), ('Chaises de bar Aledas II (lot de 2)', 139.99, 17), ('Meuble TV Molios II', 349.99, 38), ('Desserte Buddina I', 159.99, 47), ('Fauteuil de relaxation Vancouver', 199.99, 28)]

Much better !

#### Populate store inventory
Now, we will use our scraper to populate our store inventory if our inventory database is empty

```python
class Store:
    def __init__(self, name: str):
        self.name = name
        self.__inventory = []
        self.__items_count = 0

		from storify.db.inventory import InventoryFileDB, Types
        dir_path = os.path.dirname(os.path.abspath(__file__))
        self.__inventory_db = InventoryFileDB(dir_path, Types.CSV)

        data_exist = False
		for product in self.__inventory_db.load_products():
            data_exist = True
			self._append_inventory(product)

        if not data_exist:
            for product in Home24Scraper().retrieve_articles():
	            self._append_inventory(Product(*product))
	            self.save_inventory()

def add_product(self, name: str, price: float, quantity: int):
    try:
        price = float(price)
        quantity = int(quantity)

    except ValueError:
        raise ValueError(f'Invalid product input : {name}, {price}, {quantity}')

    new = Product(name, price, quantity)
    self._append_inventory(new)

    return new

def _append_inventory(self, product: Product):
    self.__inventory.append(product)
    self.__items_count += product.quantity
```

That's it ! Let's remove any inventory file left and run storify

<pre>
Welcome to OPEN Store store. Type help or ? to list commands.

Store>list_inventory
    name                                   price    quantity
--  -----------------------------------  -------  ----------
 0  Matelas confort Premium Smood         299.99          14
 1  Lit boxspring Kinx                    879.99          35
 2  Canapé convertible Latina             399.99           8
 3  Meuble TV Atelier II                  649.99          50
 4  Meuble bas Manchester I               449.99          43
 5  Meuble bas Manchester II              599.99          14
 6  Chaises de bar Aledas II (lot de 2)   139.99          20
 7  Meuble TV Molios II                   349.99           1
 8  Desserte Buddina I                    159.99          30
 9  Fauteuil de relaxation Vancouver      199.99          20
Store>
</pre>

The inventory is saved after scraping and we get an inventory file

<pre>
Matelas confort Premium Smood,299.99,14
Lit boxspring Kinx,879.99,35
Canapé convertible Latina,399.99,8
Meuble TV Atelier II,649.99,50
Meuble bas Manchester I,449.99,43
Meuble bas Manchester II,599.99,14
Chaises de bar Aledas II (lot de 2),139.99,20
Meuble TV Molios II,349.99,1
Desserte Buddina I,159.99,30
Fauteuil de relaxation Vancouver,199.99,20
</pre>