class LowerPrice(Exception):
    def __init__(self, product, price, URL):
        self.product = product
        self.price = price
        self.url = URL

    def __str__(self):
        return (
            f"Продукт: {self.product}\n"
            f"Цена: {self.price}\n"
            f"url: {self.url}\n"
            f"Проблема: цена занижена!!!"
        )


if __name__ == "__main__":
    try:
        if 1 > 0:
            raise LowerPrice("s", 2, "qwe")
    except Exception as err:
        for i in err:
            print(i)
