from bs4 import BeautifulSoup

import engine
from engine import get_html, get_product_name, script_bd, rename_dict_1

url = "https://avtodetstvo.ru/catalog/kolyaski/kol_brand-is-joie/"

MAIN_URL = "https://avtodetstvo.ru"


def get_content(html):
    soup = BeautifulSoup(html, features="lxml")
    items = soup.find_all("div", class_="item-full")
    for item in items:
        product_name = item.find("p", class_="item-full__title")
        product_price = item.find("div", class_="col-xs-5 item-full__price")
        product_url = MAIN_URL + product_name.a["href"]

        product_name = get_product_name(product_name.text)
        product_price = int(
            product_price.text.strip()[:-1]
            .strip()
            .replace("\t", "")
            .replace(" ", "")[3:]
        )
        if product_name in rename_dict_1:
            product_name = rename_dict_1[product_name]
        if product_name == "muze":
            continue
        yield script_bd(
            product_name=product_name, product_price=product_price, url=product_url
        )


def parse_text():
    error_list = []
    html = get_html(url)
    if html.status_code == 200:
        for i in get_content(html.text):
            if i is not None:
                error_list.append(i)

    else:
        print("ошибка")
    print(error_list)


def parse():
    return engine.parse(url=url, get_content=get_content)


if __name__ == "__main__":
    print(parse())
