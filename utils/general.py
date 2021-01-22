import re

from aiogram.types import User, Message
from aiogram.utils.markdown import link

import config


def get_full_name(user):
    return (user.first_name or '') + ' ' + (user.last_name or '')


def get_full_name_link(user):
    if hasattr(user, 'telegram_id'):
        user_id = user.telegram_id
    else:
        user_id = user.id
    return '<a href=\"tg://user?id=' + str(user_id) + '\">' + get_full_name(user) + '</a>'


# Сохранение медиа в канал-архив
async def save_message_to_storage_channel(target_message: Message) -> Message:
    channel_id = config.target_channel_id

    if target_message.photo:
        result_message = await target_message.bot.send_photo(chat_id=channel_id, photo=target_message.photo[-1].file_id)
    elif target_message.document:
        result_message = await target_message.bot.send_document(chat_id=channel_id, document=target_message.document.file_id)
    elif target_message.audio:
        result_message = await target_message.bot.send_audio(chat_id=channel_id, audio=target_message.audio.file_id)
    elif target_message.video:
        result_message = await target_message.bot.send_video(chat_id=channel_id, video=target_message.video.file_id)
    elif target_message.sticker:
        result_message = await target_message.bot.send_sticker(chat_id=channel_id, sticker=target_message.sticker.file_id)
    elif target_message.voice:
        result_message = await target_message.bot.send_voice(chat_id=channel_id, voice=target_message.voice.file_id)
    elif target_message.animation:
        result_message = await target_message.bot.send_animation(chat_id=channel_id, animation=target_message.animation.file_id)
    elif target_message.video_note:
        result_message = await target_message.bot.send_video_note(chat_id=channel_id, video_note=target_message.video_note.file_id)
    else:
        raise Exception('Media not found!')

    return result_message
