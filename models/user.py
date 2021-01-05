from peewee import *

from .base_model import BaseModel


class User(BaseModel):
    telegram_id = BigIntegerField(unique=True)
    first_name = TextField(null=True)
    last_name = TextField(null=True)
    username = TextField(null=True)
    premium_to = DateTimeField(null=True)
