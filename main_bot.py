import logging
import os.path
from random import random
from time import sleep
import requests
from det_mir.main import FileProcessing
from bot_engine.settings import TOKEN, scenario, generate_message
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    ConversationHandler,
    MessageHandler,
    Filters,
)
from database.bot_bd import ChatBD
from datetime import date

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# def send_typing_action(func):
#     """Sends typing action while processing func command."""
#
#     @wraps(func)
#     def command_func(update, context, *args, **kwargs):
#         context.bot.send_chat_action(
#             chat_id=update.effective_message.chat_id,
#             action=ChatAction.TYPING,
#             timeout=random() * 2 + 3,
#         )
#         return func(update, context, *args, **kwargs)
#
#     return command_func


# @send_typing_action
def start(update: Update, _: CallbackContext) -> None:
    note = ChatBD.create(
        data=date.today(),
        chat_id=update.message.chat_id,
        text="parse command",
        name=update.message.from_user,
    )
    message = (
        "Для парсинга цен на сайтах (ВНИМАНИЕ сайты будут обновляться) отправь команду - '/parse' \n"
        "Для формирования этикеток, для отгрузки заказа детского мира, отправь - '/det_mir'"
    )
    update.message.reply_text(text=message)


# @send_typing_action
def det_mir(update: Update, _: CallbackContext) -> int:
    update.message.reply_text("Отправь файл-заявку от десткого мира в формате(!) .xlsx")
    return 1


def get_file(update: Update, _: CallbackContext):
    user = update.message.document
    det_mir_xlsx = update.message.document.get_file()
    det_mir_xlsx.download(os.path.join("parser_bot", "user_file.xlsx"))
    file_path = os.path.join("parser_bot", "user_file.xlsx")
    fp = FileProcessing(file_path, "export_file")
    fp.main()
    update.message.reply_text(
        text="gВсе хорошо, файл получен, нажми '/get', чтобы получить"
    )
    return 2


def send_file(update: Update, _: CallbackContext):
    chat_id = update.message.chat_id
    file_to_send = {"document": open("bot_engine/export_file.docx", "rb")}
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendDocument?chat_id={chat_id}",
        files=file_to_send,
    )


# @send_typing_action
def parse(update: Update, _: CallbackContext) -> None:
    ChatBD.create(
        data=date.today(),
        chat_id=update.message.chat_id,
        text="parse command",
        name=update.message.from_user,
    )
    keyboard = [
        [
            InlineKeyboardButton("Первая коляска", callback_data="pervaya_kolyaska"),
            InlineKeyboardButton("Мир автокресел", callback_data="mir_avtokresel"),
        ],
        [
            InlineKeyboardButton("Роял кид", callback_data="royal_kids"),
            InlineKeyboardButton("Алло Мама", callback_data="allomama"),
        ],
        [InlineKeyboardButton("Автодетство", callback_data="avtodetstvo")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Выбери сайт для парсинга цен.\n"
        "Eсли нужно проверить все, отправь команду '/all'",
        reply_markup=reply_markup,
    )


# @send_typing_action
def button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query

    query.answer()
    error_list = scenario[query.data]()

    note = ChatBD.create(
        data=date.today(),
        chat_id=update.callback_query.message.chat_id,
        text=query.data,
        name=query.message.from_user,
    )

    sleep(random() * 2 + 3.0)

    query.edit_message_text(
        text=generate_message(scenario[query.data], error_list),
        disable_web_page_preview=True,
    )


# @send_typing_action
def help_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Используй /start для начала парсинга")


# @send_typing_action
def all_command(update: Update, _: CallbackContext):
    for message in scenario["all"]():
        update.message.reply_text(text=message, disable_web_page_preview=True)


def main() -> None:
    updater = Updater(TOKEN)
    conv = ConversationHandler(
        entry_points=[CommandHandler("det_mir", det_mir)],
        states={
            1: [MessageHandler(Filters.document, get_file)],
            2: [CommandHandler("get", send_file)],
        },
        fallbacks=[
            CommandHandler("start", start),
        ],
    )
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("parse", parse))
    updater.dispatcher.add_handler(CommandHandler("all", all_command))
    updater.dispatcher.add_handler(conv)

    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler("help", help_command))

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
