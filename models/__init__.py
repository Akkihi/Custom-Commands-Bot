import os
from typing import Union

import aiogram
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


def save_user(user: aiogram.types.User):
    db_user, created = User.get_or_create(telegram_id=user.id)
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.username = user.username
    db_user.save()

    return db_user, created


def save_chat(chat: aiogram.types.Chat):
    db_chat, created = Chat.get_or_create(telgram_id=chat.id)
    db_chat.title = chat.title
    db_chat.link = chat.invite_link
    db_chat.save()

    return db_chat, created


def save_command(trigger,
                 text,
                 media: Union[aiogram.types.Document,
                              aiogram.types.PhotoSize,
                              aiogram.types.Audio],
                 created_by: aiogram.types.User,
                 to_chat: aiogram.types.Chat = None,
                 is_inline=False,
                 is_reply=False):
    db_user, created = save_user(created_by)

    if to_chat:
        db_chat, created = save_chat(to_chat)
    else:
        db_chat = None

    db_command, created = Command.get_or_create(created_by=db_user,
                                                to_chat=db_chat,
                                                trigger=trigger,
                                                is_inline=is_inline,
                                                is_reply=is_reply)
    db_command.text = text
    db_command.media_file_id = media.file_id

    if isinstance(media, aiogram.types.Document):
        db_command.media_type = 'document'
    if isinstance(media, aiogram.types.PhotoSize):
        db_command.media_type = 'photo'
    if isinstance(media, aiogram.types.Audio):
        db_command.media_type = 'audio'

    db_command.save()

    return db_command, created
