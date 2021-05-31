import os

from peewee import *
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE_DIR, "chat.db")
db = SqliteDatabase(path)


class ChatBD(Model):
    data = DateField()
    chat_id = IntegerField()
    text = CharField()

    class Meta:
        database = db


if __name__ == '__main__':
    print(date.today())