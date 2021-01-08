
from aiogram.types import Message
from aiogram.dispatcher.handler import SkipHandler

from auth import dp
from models import save_chat, save_user, Command
from utils.general import get_full_name


@dp.message_handler(lambda msg: msg.is_command())
async def on_trigger(message: Message):
    trigger = message.get_command()[1:]
    db_user, created = save_user(message.from_user)
    db_chat, created = save_chat(message.chat)
    chat_id = message.chat.id
    try:
        command = Command.get((Command.created_by == db_user)
                              & (Command.to_chat == db_chat)
                              & (Command.is_inline == False)
                              & (Command.trigger == trigger))
    except Exception as e:
        print(e)
        raise SkipHandler

    if command.is_reply and not message.reply_to_message:
        await message.answer('Комманда должна быть отправлена ответом на сообщение')
        return

    try:
        await message.delete()
    except:
        pass

    if command.text:
        caption = get_full_name(message.from_user) + ' ' + command.text
        if command.is_reply:
            caption += ' ' + get_full_name(message.reply_to_message.from_user)
    else:
        caption = None

    if command.media_type == 'photo':
        await message.bot.send_photo(chat_id=chat_id, photo=command.media_file_id, caption=caption)
    if command.media_type == 'document':
        await message.bot.send_document(chat_id=chat_id, document=command.media_file_id, caption=caption)
    if command.media_type == 'audio':
        await message.bot.send_audio(chat_id=chat_id, audio=command.media_file_id, caption=caption)
    if command.media_type == 'video':
        await message.bot.send_video(chat_id=chat_id, video=command.media_file_id, caption=caption)
    if command.media_type == 'sticker':
        await message.bot.send_sticker(chat_id=chat_id, sticker=command.media_file_id)
    if command.media_type == 'voice':
        await message.bot.send_voice(chat_id=chat_id, voice=command.media_file_id, caption=caption)
    if command.media_type == 'animation':
        await message.bot.send_animation(chat_id=chat_id, animation=command.media_file_id, caption=caption)
    if command.media_type == 'video_note':
        await message.bot.send_video_note(chat_id=chat_id, video_note=command.media_file_id)
    if command.media_type == 'no_media':
        await message.bot.send_message(chat_id=chat_id, text=caption)

