import logging
from settings import TOKEN, scenario, generate_message
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, _: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Первая коляска", callback_data="pervaya_kolyaska"),
            InlineKeyboardButton("Мир автокресел", callback_data="mir_avtokresel"),
        ],
        [
            InlineKeyboardButton("Роял кид", callback_data="royal_kids"),
            InlineKeyboardButton("Алло Мама", callback_data="allomama"),
        ],
        [
            InlineKeyboardButton("Автодетство", callback_data="avtodetstvo")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Выбери сайт для парсинга цен.\n"
                              "Eсли нужно проверить все, отправь команду '/all'",
                              reply_markup=reply_markup)


def button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query

    query.answer()
    error_list = scenario[query.data]()

    query.edit_message_text(
        text=generate_message(scenario[query.data], error_list),
        disable_web_page_preview=True,
    )


def help_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Используй /start для начала парсинга")


def all_command(update: Update, _: CallbackContext):
    # message = scenario['all']()
    for message in scenario["all"]():
        update.message.reply_text(text=message, disable_web_page_preview=True)


def main() -> None:
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("all", all_command))

    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler("help", help_command))

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
