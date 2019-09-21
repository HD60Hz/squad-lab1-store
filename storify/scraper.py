import random
import re
import time
from enum import Enum
from typing import Iterable

import requests
from bs4 import BeautifulSoup


class Home24Categories(Enum):
    MEUBLE = 'https://www.home24.fr/categorie/meubles/'
    JARDIN = 'https://www.home24.fr/categorie/jardin/'
    LUMINAIRE = 'https://www.home24.fr/categorie/luminaires/'


class Home24Scraper:
    def __init__(self, category: Home24Categories):
        self.__category = category

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
