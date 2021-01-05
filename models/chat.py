from peewee import *

from .base_model import BaseModel


class Chat(BaseModel):
    telegram_id = BigIntegerField(unique=True)
    title = TextField(null=True)
    premium_to = DateTimeField()
