from peewee import *

from .base_model import BaseModel
from .user import User
from .chat import Chat


class Command(BaseModel):
    created_by = ForeignKeyField(User, backref='commands', on_delete='CASCADE')
    to_chat = ForeignKeyField(Chat, backref='commands', on_delete='CASCADE')
    trigger = textField(null=True)
    text = TextField(null=True)
    media_file_id = BigIntegerField(null=True)
    media_type = TextField(null=True)
    is_inline = BooleanField(default=False)
    is_reply = BooleanField(default=False)
