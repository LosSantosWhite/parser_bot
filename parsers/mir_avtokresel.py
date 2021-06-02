from pprint import pprint

import bs4

import engine
from engine import get_product_name, get_html, check_price_from_db, rename_dict_1

URL = "https://www.mir-avtokresel.ru/catalog/joie-detskie-avtokresla/"
MAIN_URL = "https://www.mir-avtokresel.ru"


def get_content(html):
    soup = bs4.BeautifulSoup(html, "lxml")
    items = soup.find_all("div", class_="main")
    error_product = []

    for item in items:

        product_url = MAIN_URL + item.a["href"]
        item = item.text.replace("\n", "")
        item = item.split(" ")
        product_name = ""
        product_price = ""
        # Из спика [...'24', '000', '']] возвращает цену
        for price in item[-3:]:
            product_price += price
        # Из спика ['Joie', 'Mytrax', ...] Делает название Joie Mytrax etc.
        for name in item[:-3]:
            product_name += name + " "
        product_name = get_product_name(product_name)
        product_price = int(product_price)

        if product_name in rename_dict_1:
            product_name = rename_dict_1[product_name]

        try:
            check_price_from_db(product_name, product_price, product_url)
        except Exception as err:
            params = (product_name, product_price, product_url, err)
            yield params


def parse():
    return engine.parse(url=URL, get_content=get_content)


if __name__ == "__main__":
    print(parse())
