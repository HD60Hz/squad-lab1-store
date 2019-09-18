import random
import re
from typing import Iterable

import requests
from bs4 import BeautifulSoup


class Home24Scraper:
    url_target = 'https://www.home24.fr/categorie/meubles/'

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


if __name__ == '__main__':
    print(Home24Scraper().retrieve_articles())
