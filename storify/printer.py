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
