from pprint import pprint

import bs4

import engine
from Errors.custom_errors import LowerPrice
from engine import get_product_name, check_price_from_db, rename_dict_1, get_html

MAIN_URL = "https://www.first-buggy.ru"
URL = (
    "https://www.first-buggy.ru/catalog/Joie/",
    "https://www.first-buggy.ru/catalog/Joie/?page_4=2",
)


def get_content(html):
    soup = bs4.BeautifulSoup(html, "lxml")
    items = soup.find_all("div", class_="main")
    error_product = []
    for item in items:

        if "2-in-1" in item.a["href"]:
            continue
        elif "2in1" in item.a["href"]:
            continue
        else:
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

            product_price = product_price.replace(" ", "")

            if "атрасик-муфта" in product_name and "2900" in product_price:
                product_name = "footmuff"
            elif "атрасик-муфта" in product_name and "3500" in product_price:
                product_name = "versatrax footmuff"
            elif "ёплый конверт" in product_name and "6400" in product_price:
                product_name = "THERMA WINTER FOOTMUFF"

            product_name = get_product_name(product_name)
            product_price = int(product_price)

            if product_name in rename_dict_1:
                product_name = rename_dict_1[product_name]
                product_name = get_product_name(product_name)

            try:
                check_price_from_db(product_name, product_price, product_url)
            except LowerPrice:
                params = (product_name, product_price, product_url)
                yield params


def parse():
    error_list = []
    for url in URL:
        html = get_html(url)
        if html.status_code == 200:
            for err in get_content(html.text):
                if err is not None:
                    error_list.append(err)
        else:
            print("Dostypa net")
    return error_list


if __name__ == "__main__":
    a = parse()
    pprint(a)
