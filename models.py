import datetime
from peewee import *
from flask_login import UserMixin
from playhouse.postgres_ext import *

DATABASE = PostgresqlExtDatabase(
    'car_app',
    user='ian',
    password='password',
    host='localhost'
)

class User(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        db_table = 'users'
        database = DATABASE

class Car(Model):
    make = CharField()
    model = CharField()
    year = IntegerField()
    data = JSONField(default={})
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'cars'
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Car], safe=True)
    print("TABLES Created")
    DATABASE.close()