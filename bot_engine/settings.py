import parsers.pervaya_kolyaska as pk
import parsers.royal_kids as rk
import parsers.mir_avtokresel as mk
import parsers.allomama as am
import parsers.avtodetstvo as at

TOKEN = "1637081624:AAGBlnEcbhOnLQHyMyuomJPggrsqr0H5oQo"


def generate_message(func, errors: list) -> str:
    message = ""
    for error in errors:
        try:
            message += (
                f"Название: {error[0]}, \n"
                f"Цена: {error[1]}, \n"
                f"Сcылка: {error[2]} \n"
            )
        except Exception as err:
            print(error, err)
    if message == "":
        message = f"Все Ок ✅✅✅\n"
    message += "Отправь '/start' для повтора\n"
    return message


def run_all_parsers() -> str:
    func_list = [pk, mk, am, rk, at]
    for i in func_list:
        error_list = i.parse()
        message = "{:*^33}\n".format(i.__name__[8:], "centered")
        message += generate_message(func=i, errors=error_list)

        yield message


scenario = {
    "pervaya_kolyaska": pk.parse,
    "mir_avtokresel": mk.parse,
    "royal_kids": rk.parse,
    "allomama": am.parse,
    "avtodetstvo": at.parse,
    "all": run_all_parsers,
}

if __name__ == "__main__":
    print(run_all_parsers())
