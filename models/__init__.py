import os

from peewee import *

from .base_model import BaseModel, DATABASE
from .user import User
from .chat import Chat
from .command import Command


if not os.path.exists(DATABASE):
    db = SqliteDatabase(DATABASE)
    db.create_tables([
        User,
        Chat,
        Command,
    ])

