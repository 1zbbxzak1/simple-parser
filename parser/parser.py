import requests
from bs4 import BeautifulSoup

from db.model import Product


def parser_products():
    url = 'https://www.maxidom.ru/catalog/svarochnoe-oborudovanie/'

    while url:
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        category_tag = soup.find("span", itemprop="name")
        category = category_tag.get_text(strip=True) if category_tag else "No category"

        items = soup.find_all('article', class_='l-product')
        for item in items:
            # Извлекаем название по атрибуту `itemprop="name"`
            name_tag = item.find('span', itemprop='name')
            name = name_tag.get_text(strip=True) if name_tag else "No name"

            # Извлекаем цену товара
            price_tag = item.find('span', itemprop='price')
            price = price_tag.get_text(strip=True) if price_tag else "No price"

            # Проверка на дублирование в БД перед добавлением
            if not Product.exists(name, price):
                Product.save_product(category, name, price)
            else:
                print(f"Skipping duplicate product: {name} - {price}")

        # Переход на следующую страницу, если есть
        next_page = soup.select_one('#navigation_2_next_page[href]')
        if next_page:
            url = "https://www.maxidom.ru" + next_page['href']
        else:
            url = None  # Завершить цикл, если следующей страницы нет
