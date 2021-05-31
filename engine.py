import requests
from database.create_db_from_file import RRP
from Errors.custom_errors import LowerPrice

rename_dict_1 = {
    "i-gemm": "i-gemm 2",
    "traver isofix": "traver",
    "i-level + база": "i-level",
    "sansa 2 в 1": "sansa 2in1",
    "Multiply": "multiply 6in1",
    "ramble": "RAMBLE CC match L4, MYTRAX",
    "chrome carrycot": "chrome carry cot",
    "tourist signature": "tourist flex signature",
    "mimzy 360": "mimzy spin 3in1",
    "multiply 6 в 1": "multiply 6in1",
    "multiply": "multiply 6in1",
    "mimzy lx": "mimzy 2in1",
    "mimzy spin": "mimzy spin 3in1",
    "ramble carry cot": "ramble cc match l4, mytrax",
    "universal footmuff signature": "signature footmuff signature",
    "ramble xl signature": "ramble xl carry cot flex signature",
    "ramble xl carry cot": "ramble xl",
    "chrome сarry сot dlx": "chrome carry cot",
    "footmuff": "litetrax footmuff",
    "": "versatrax footmuff",
    "sansa swing": "sansa 2in1",
    "adapter for car seat & carry cot accessory": "litetrax 4 adapter v2",
    "litetrax 3, litetrax 4, litetrax 4 air footmuff": "litetrax footmuff",
    "chrome dlx footmuff": "chrome carry cot",
    "airetwin": "aire twin",
    "aireskip": "aire skip",
    "serina": "serina 2in1",
    "stroller pact": "pact"
}


def get_product_price(price: str) -> int:
    price = price.strip()[:-4]
    if len(price) > 10:
        price = price.split("руб.")[1]
    price = price.replace(" ", "")
    return int(price)


def get_product_name(product_name: str, category=None) -> str:
    ignore_names = (
        "gray",
        "lychee",
        "ember",
        "navy blaczer",
        "pavement",
        "pastel forest",
        "little world",
        "in the rain",
        "123 artwork",
        "petite city",
        "dark pewter",
        "rosy & sea",
        "cranberry",
        "tuxedo",
        "lilac",
    )
    product_name = product_name.lower()
    if "joie" in product_name:
        product_name = product_name.split("joie")[1]
    product_name = product_name.split("(")[0]
    product_name = product_name.split(" – ")[0]
    product_name = product_name.split(" - ")[0]
    product_name = product_name.replace("i-size", "")
    product_name = product_name.replace("  ", " ")
    if "w/" in product_name:
        product_name = product_name.split("w/")[0]
        product_name = product_name[1:]
    if category == "SIGNATURE SERIES Кресла" or category == "SIGNATURE SERIES Коляски":
        product_name = product_name + " signature"
    product_name = product_name.strip()
    product_name = product_name.replace("  ", " ")
    return product_name


HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 "
                  "(KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "accept": "*/*",
}


def get_html(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    return response


def check_price_from_db(product_name: str, product_price: int, url: str):
    product_from_db = RRP.get(RRP.name == product_name)
    if product_from_db.price != product_price:
        raise LowerPrice(product_name, product_price, url)


def script_bd(product_name: str, product_price: int, url="") -> tuple:
    try:
        check_price_from_db(product_name, product_price, url)
    except LowerPrice:
        params = (product_name, product_price, url)
        return params


def parse(url, get_content):
    error_list = []
    html = get_html(url)
    if html.status_code == 200:
        for err in get_content(html.text):
            if err is not None:
                error_list.append(err)
    else:
        print("Dostypa net")
    return error_list


if __name__ == "__main__":
    pass
