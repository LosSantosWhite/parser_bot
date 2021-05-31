from engine import (
    get_html,
    get_product_name,
    get_product_price,
    script_bd,
    rename_dict_1,
)
from bs4 import BeautifulSoup

URL = "https://allomama.ru/Joie-velikobritaniya-"


def get_content(html):
    soup = BeautifulSoup(html, "lxml")
    items = soup.find_all("div")
    exclude = (
        "litetrax 4, litetrax 4 air",
        "на коляски float/aire lite/ aire skip/ sma baggi",
        "trillo eco",
        "muze",
        "sma baggi",
        "aireskip",
        "float",
    )
    prev_name = None
    for item in items:

        name = item.find("div", class_="name")
        price = item.find("div", class_="price")

        if name is None or price is None:
            continue
        else:
            name = get_product_name(name.text)
            if name == prev_name:
                continue
            price = get_product_price(price.text)
            url = item.find("div", class_="name").a["href"]
            if name in exclude:
                continue
            if name in rename_dict_1:
                name = rename_dict_1[name]
            prev_name = name
            yield script_bd(name, price, url)


def parse():
    html = get_html(URL)
    error_list = []
    if html.status_code == 200:
        for element in get_content(html.text):
            if element is not None:
                error_list.append(element)
    else:
        return ["Dostypa net", html.status_code, URL]

    return error_list


if __name__ == "__main__":
    print(parse())
