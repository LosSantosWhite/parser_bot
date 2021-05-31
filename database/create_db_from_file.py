from peewee import *
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE_DIR, "price.db")
# path = os.path.join("database", "price.db")
db = SqliteDatabase(path)


class RRP(Model):
    name = CharField()
    price = IntegerField()

    class Meta:
        database = db


if __name__ == "__main__":
    db.create_tables([RRP])
