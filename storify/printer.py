from datetime import date
import random
import time
from pathlib import Path
from typing import List

import jinja2
import pdfkit

from storify import DATA_DIR
from storify.store import Purchase

INVOICE_TEMPLATE_FILE = 'invoice.html'
ITEM_TEMPLATE_FILE = 'item.html'


class InvoicePrinter:
    def __init__(self, store_name):
        self.title = store_name
        self.template_dir = Path(__file__).parent / 'templates'
        self.invoice_dir = DATA_DIR / 'invoices'
        self.invoice_dir.mkdir(parents=True, exist_ok=True)

    def print(self, purchases: List[Purchase], total: int):
        template_loader = jinja2.FileSystemLoader(searchpath=str(self.template_dir))
        template_env = jinja2.Environment(loader=template_loader)

        invoice_template = template_env.get_template(INVOICE_TEMPLATE_FILE)
        item_template = template_env.get_template(ITEM_TEMPLATE_FILE)

        items_output = ''
        for purchase in purchases:
            items_output += item_template.render(
                name=purchase.name,
                rate=purchase.price,
                quantity=purchase.quantity,
                price=purchase.price * purchase.quantity
            )

        output = invoice_template.render(
            id=random.randint(1000, 10000),
            title=self.title,
            total=total,
            items=items_output,
            today=date.today().strftime('%d, %b %Y')
        )

        pdfkit.from_string(output, self.invoice_dir / f'invoice_{time.strftime("%Y%m%d-%H%M%S")}.pdf')
