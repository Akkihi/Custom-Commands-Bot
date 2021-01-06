from aiogram.types import User, Message

import config


def get_full_name(user: User):
    return (user.first_name or '') + ' ' + (user.last_name or '')


async def save_message_to_storage_channel(target_message: Message) -> Message:
    channel_id = config.target_channel_id

    if target_message.photo:
        result_message = await target_message.bot.send_photo(chat_id=channel_id, photo=target_message.photo[-1].file_id)
    elif target_message.document:
        result_message = await target_message.bot.send_document(chat_id=channel_id, document=target_message.document.file_id)
    elif target_message.audio:
        result_message = await target_message.bot.send_audio(chat_id=channel_id, audio=target_message.audio.file_id)
    else:
        raise Exception('Media not found!')

    return result_message
