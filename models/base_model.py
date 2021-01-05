from peewee import *

DATABASE = 'database.db'
db = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        database = db
