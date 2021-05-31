from pprint import pprint

import engine
from Errors.custom_errors import LowerPrice
from engine import get_product_name, get_html, check_price_from_db, rename_dict_1, parse
from bs4 import BeautifulSoup

URL = "https://royal-kid.com/joie"


def get_content(html):
    soup = BeautifulSoup(html, "lxml")
    items = soup.find_all("div", class_="item")
    for item in items:
        if "2 в 1" in item.text:
            continue
        elif r"\n" == item.text:
            continue
        else:
            product_name = item.find("div", class_="name").text[:-1]
            product_url = item.a["href"]
            product_name = get_product_name(product_name)
            product_price = int(item.find("div", class_="price").text[1:-3])

            if product_name in rename_dict_1:
                product_name = rename_dict_1[product_name]

            try:
                check_price_from_db(product_name, product_price, product_url)
            except LowerPrice:
                params = (product_name, product_price, product_url)
                yield params


def parse():
    return engine.parse(
        url=URL,
        get_content=get_content
    )


if __name__ == "__main__":
    pprint(parse(url=URL, get_content=get_content))
