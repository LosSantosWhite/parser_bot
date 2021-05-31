import unittest

from bs4 import BeautifulSoup

from engine import get_product_name

url = "test link"
prices = {"i-level": 33000, "traver": 20000, "litetrax 4": 15600, "mytrax": 24000}

test_element = (
    '<div class="main">'
    '<a class="font-r" '
    'href="/catalog/detail/Joie/Joie-Mytrax/" '
    'onclick="PK.catalog.clickProduct($(this))" '
    'title="Joie Mytrax – цена, характеристики, обзоры, отзывы">Joie Mytrax</a>'
    '<div class="price font-r"> <span class="cur-price">24 000 <i class="fa fa-rub">'
    "</i></span></div></div>"
)


# Тесты на сайт Первая коляска РФ
class Parsing(unittest.TestCase):
    soup = BeautifulSoup(test_element, "lxml")
    item = soup.find_all("div", class_="main")[0]

    def test_first(self):
        self.assertEqual(get_product_name("Mytrax Flex"), "mytrax flex")

    def test_second(self):
        self.assertEqual(
            get_product_name("Joie Mytrax Flex Signature"), "mytrax flex signature"
        )

    def test_third(self):
        self.assertEqual(
            get_product_name("Коляска крутая Joie Litetrax 4 "), "litetrax 4"
        )

    def test_fourth(self):
        self.assertEqual(
            get_product_name("Автокресло Joie i-Spin 360 E"), "i-spin 360 e"
        )

    def test_fifth(self):
        self.assertEqual(get_product_name("Traver "), "traver")

    def test_w_slash(self):
        self.assertEqual(get_product_name("joie Versatrax W/ RC"), "versatrax")

    def test_carseat_signature(self):
        self.assertEqual(
            get_product_name("i-spin 360", "SIGNATURE SERIES Кресла"),
            "i-spin 360 signature",
        )

    def test_sixth(self):
        self.assertEqual(get_product_name("i-spin 360 (group 1/2/3)"), "i-spin 360")

    def test_bs4(self):
        self.assertEqual(self.item.a["href"], "/catalog/detail/Joie/Joie-Mytrax/")

    def test_func(self):
        self.assertEqual(get_product_name(self.item.a["title"]), "mytrax")
