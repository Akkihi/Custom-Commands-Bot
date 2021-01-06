from peewee import *

from .base_model import BaseModel
from .user import User
from .chat import Chat


class Command(BaseModel):
    created_by = ForeignKeyField(User, backref='commands', on_delete='CASCADE')
    chat = ForeignKeyField(Chat, backref='commands', on_delete='CASCADE')
    text = TextField(null=True)
    media_msg_id = BigIntegerField(null=True)
    is_inline = BooleanField(default=False)
    is_reply = BooleanField(default=False)
