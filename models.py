import os 
import datetime
from peewee import *
from flask_login import UserMixin
from playhouse.postgres_ext import *
from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
    DATABASE = PostgresqlExtDatabase(
        'car_app',
        user='ian',
        password='password',
        host='localhost'
    )

class User(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField()

    def __str__(self):
        return '<User: {}, id: {}>'.format(self.email, self.id)

    def __repr__(self):
        return '<User: {}, id: {}>'.format(self.email, self.id)

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

class SavedCar(Model):
    event_id = AutoField()
    make = CharField()
    model = CharField()
    year = IntegerField()
    data = JSONField(default={})
    owner = ForeignKeyField(User, backref='cars')
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'savedcars'
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Car, SavedCar], safe=True)
    print("TABLES Created")
    DATABASE.close()