LAB1 SQUAD TRAINING - PYTHON
---

### Invoice
After shopping in our store, the least we can do is provide the customer with his due invoice. We will go with one of the most popular document format: **PDF**  

There are many Python libraries to manage PDFs: _FPDF, pyPDF, Reportlab, PrinceXML, Weasyprint, pdfkit_... from small and easy to use to professional with complete features.  
The problem and use case at hand will help you filter:  
* Create PDF from scratch VS alter existing one
* Use of programmatic API to construct the document VS use of markup language (ex: RML) 
* Generate from simpler format (ex: HTML)  
...

Anyway, in this lab we are going the super easy route. So we are going to create our invoice using ``pdfkit`` from an ``jinja2`` generated HTML

#### Invoice Template

[Jinja2](https://jinja.palletsprojects.com/en/2.10.x/) is very powerfull and widely used templating engine for Python. We will use it to fill placeholders inside our invoice template

To install Jinja run the command

```shell script
pip install jinja2
```

To install pdfkit run the command

```shell script
pip install pdfkit
```

pdfkit uses [wkhtmltopdf](https://wkhtmltopdf.org/index.html) internally for HTML to PDF conversion. We need to [install](https://wkhtmltopdf.org/downloads.html) it

Next, let's create ``invoice.html`` inside a templates folder and a ``printer`` module

Result (file system):
<pre>
storify
    ├── ...
    ├── printer.py
    ├── store.py
    └── templates
        └── invoice.html
</pre>

The information that our invoice will hold are:
* Title
* Invoice id
* Current date
* Total of purchases

For each purchase 
* Name
* Rate
* Quantity
* Price

```html
<html>
<head>
    <meta charset="utf-8">
    <title>Invoice</title>
</head>
<body>
<article>
    <h1>{{ title }}</h1>
    <table class="meta">
        <tr>
            <th><span contenteditable>Invoice #</span></th>
            <td><span contenteditable>{{ id }}</span></td>
        </tr>
        <tr>
            <th><span contenteditable>Date</span></th>
            <td><span contenteditable>{{ today }}</span></td>
        </tr>
        <tr>
            <th><span contenteditable>Amount Due</span></th>
            <td><span id="prefix" contenteditable>$</span><span>{{ total }}</span></td>
        </tr>
    </table>
    <table class="purchases">
        <thead>
        <tr>
            <th><span contenteditable>Item</span></th>
            <th><span contenteditable>Rate</span></th>
            <th><span contenteditable>Quantity</span></th>
            <th><span contenteditable>Price</span></th>
        </tr>
        </thead>
        <tbody>
        {% for purchase in purchases %}
        <tr>
            <td><a class="cut">-</a><span contenteditable>{{ purchase['name'] }}</span></td>
            <td><span data-prefix>$</span><span contenteditable>{{ purchase['rate'] }}</span></td>
            <td><span contenteditable>{{ purchase['quantity'] }}</span></td>
            <td><span data-prefix>$</span><span>{{ purchase['price'] }}</span></td>
        </tr>
        {% endfor %}
        </tbody>
    </table>
    <a class="add">+</a>
    <table class="balance">
        <tr>
            <th><span contenteditable>Total</span></th>
            <td><span data-prefix>$</span><span>{{ total }}</span></td>
        </tr>
    </table>
</article>
</body>
</html>
```

#### Printer

Next we will create the ``InvoicePrinter`` in our ``printer`` module. Obviously, this printer will have a ``print`` method

```python
import random
import time
from datetime import date
from pathlib import Path
from typing import List

import jinja2
import pdfkit

from storify import DATA_DIR
from storify.store import Purchase, Store

INVOICE_TEMPLATE_FILE = 'invoice.html'
INVOICE_DIRNAME = 'invoices'
INVOICE_PREFIX = 'invoice'

class InvoicePrinter:
    def __init__(self, title):
        self.__title = title
        self.__invoice_dir = DATA_DIR / INVOICE_DIRNAME
        self.__invoice_dir.mkdir(parents=True, exist_ok=True)

        template_dir = Path(__file__).parent / 'templates'
        template_loader = jinja2.FileSystemLoader(searchpath=str(template_dir))
        template_env = jinja2.Environment(loader=template_loader)
        self.__invoice_template = template_env.get_template(INVOICE_TEMPLATE_FILE)

    def print(self, purchases: List[Purchase], total: int):
        output = self.__invoice_template.render(
            id=random.randint(1000, 10000),
            title=self.__title,
            total=total,
            today=date.today().strftime('%d, %b %Y'),
            purchases=({
                'name': purchase.name,
                'rate': purchase.price,
                'quantity': purchase.quantity,
                'price': purchase.price * purchase.quantity
            } for purchase in purchases)
        )

        pdfkit.from_string(output, self.__invoice_dir / f'{INVOICE_PREFIX}_{time.strftime("%Y%m%d-%H%M%S")}.pdf')
```

In the initialization phase, after resolving and creating the _invoice directory_ inside the data folder. We create the Jinja file system loader and we point it to our ``templates`` folder. After that we create the jinja environment that will compile and create the template objects internally  
We keep reference of the invoice template object

When a ``print`` is requested, we simply render the invoice with all the provided data. The output is fed to _pdfkit_ to generate the invoice PDF

#### Invoice on checkout
While initializing the store, we will create the invoice printer with store name as the title. The printer is used at the end of the checkout

```python
class Store:
    def __init__(self, name: str):
        ...
        from storify.printer import InvoicePrinter
        self.__invoice_printer = InvoicePrinter(self.name)
        ...

     def checkout(self, cart):
        ...

        self.__invoice_printer.print(purchases, total)

        return purchases, total
```

Let's test it 

Result:
<pre>
Store>simulate_customer
Customer>pick_product
Choose a product> 3
Picking product : Product(id=3, name='Lit boxspring Kinx', price=879.99, quantity=19)
How many? 2
Customer>pick_product
Choose a product> 1
Picking product : Product(id=1, name='Suspension Brooklyn I', price=219.99, quantity=14)
How many? 1
Customer>checkout
qt5ct: using qt5ct plugin
qt5ct: D-Bus system tray: no
Loading page (1/2)
Printing pages (2/2)
Done
You have purchased:
Lit boxspring Kinx 879.99 x 2
Suspension Brooklyn I 219.99 x 1
Total: 1979.97
Customer>
</pre>

Result (file system):
<pre>
data
│   ├── inventory.csv
│   └── invoices
│       ├── invoice_20190902-003536.pdf
│       ├── invoice_20190902-025134.pdf
│       ├── invoice_20190902-025245.pdf
│       ├── invoice_20190902-025505.pdf
│       └── invoice_20190902-112034.pdf
...
</pre>

Again, because we have new dependencies, we have to update ``requirements.txt``

```shell script
pip freeze > requirements.txt
```