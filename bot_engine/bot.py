import logging
from random import random
from time import sleep

from settings import TOKEN, scenario, generate_message
from functools import wraps
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, bot, ChatAction
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from database.bot_bd import ChatBD
from datetime import date

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING,
                                     timeout=random()*2+3)
        return func(update, context, *args, **kwargs)

    return command_func


@send_typing_action
def start(update: Update, _: CallbackContext) -> None:
    note = ChatBD.create(data=date.today(),
                         chat_id=update.message.chat_id,
                         text='start command')
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


@send_typing_action
def button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query

    query.answer()
    error_list = scenario[query.data]()

    note = ChatBD.create(data=date.today(),
                         chat_id=update.callback_query.message.chat_id,
                         text=query.data)

    sleep(random() * 2 + 3.)

    query.edit_message_text(
        text=generate_message(scenario[query.data], error_list),
        disable_web_page_preview=True,
    )


@send_typing_action
def help_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Используй /start для начала парсинга")


@send_typing_action
def all_command(update: Update, _: CallbackContext):
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
