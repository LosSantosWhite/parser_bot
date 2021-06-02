import os

from peewee import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE_DIR, "chat.db")
db = SqliteDatabase(path)


class ChatBD(Model):
    data = DateField()
    chat_id = IntegerField()
    name = CharField()
    text = CharField()

    class Meta:
        database = db


if __name__ == "__main__":
    db.create_tables([ChatBD])
