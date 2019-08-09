import requests
from bs4 import BeautifulSoup

url = "https://www.fnac.com/musique.asp#bl=MMmu"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

response = requests.get(url, headers=headers)
content = response.content

soup = BeautifulSoup(content, features="lxml")

body = soup.find_all("div", {"class": "Category-item"})

print(body)

