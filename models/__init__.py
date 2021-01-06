import os
from typing import Union, List

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
    db_chat, created = Chat.get_or_create(telegram_id=chat.id)
    db_chat.title = chat.title
    db_chat.link = chat.invite_link
    db_chat.save()

    return db_chat, created


def save_command(trigger,
                 created_by: aiogram.types.User,
                 to_chat: aiogram.types.Chat,
                 text=None,
                 media: Union[aiogram.types.Document,
                              List[aiogram.types.PhotoSize],
                              aiogram.types.Audio,
                              aiogram.types.Voice,
                              aiogram.types.Sticker,
                              aiogram.types.Video,
                              aiogram.types.VideoNote,
                              aiogram.types.Animation] = None,
                 is_inline=False,
                 is_reply=False):
    db_user, created = save_user(created_by)
    db_chat, created = save_chat(to_chat)

    db_command, created = Command.get_or_create(created_by=db_user,
                                                to_chat=db_chat,
                                                trigger=trigger,
                                                is_inline=is_inline,
                                                is_reply=is_reply)
    if text:
        db_command.text = text

    if media:
        if isinstance(media, aiogram.types.Document):
            db_command.media_type = 'document'
        if isinstance(media, List):
            db_command.media_type = 'photo'
            media = media[-1]
        if isinstance(media, aiogram.types.Audio):
            db_command.media_type = 'audio'
        if isinstance(media, aiogram.types.Voice):
            db_command.media_type = 'voice'
        if isinstance(media, aiogram.types.Video):
            db_command.media_type = 'video'
        if isinstance(media, aiogram.types.VideoNote):
            db_command.media_type = 'video_note'
        if isinstance(media, aiogram.types.Animation):
            db_command.media_type = 'animation'
        if isinstance(media, aiogram.types.Sticker):
            db_command.media_type = 'sticker'

        db_command.media_file_id = media.file_id

    db_command.save()

    return db_command, created
