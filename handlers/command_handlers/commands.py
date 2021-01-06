import models
from aiogram.types import Message, ChatType
from auth import dp
from utils.general import save_message_to_storage_channel


@dp.message_handler(commands=['add', 'addr'], chat_type=[ChatType.PRIVATE, ChatType.GROUP])
async def add_command(message: Message):
    target_message = message.reply_to_message
    if not target_message:
        await message.answer('Команда должна быть ответом на сообщение')
        return

    trigger = message.get_args()
    if not trigger:
        await message.answer('Триггер после комманды не указан')
        return

    text = target_message.text

    is_reply = message.get_command()[1:] == 'addr'

    media = None
    if target_message.photo or target_message.document or target_message.audio:
        media_message = await save_message_to_storage_channel(message.reply_to_message)
        media = media_message.audio or media_message.document or media_message.photo

    is_command_inline = False
    if message.chat.type == ChatType.PRIVATE:
        is_command_inline = True

    models.save_command(trigger=trigger,
                        text=text,
                        media=media,
                        created_by=message.from_user,
                        to_chat=message.chat,
                        is_inline=is_command_inline,
                        is_reply=is_reply)

    await message.reply(text='Команда добавлена.')


@dp.message_handler(commands='del', chat_type=ChatType.GROUP)
async def delete_command(message: Message):
    await message.reply(text='Команда удалена.')


@dp.message_handler(commands='get_id', chat_type=ChatType.GROUP)
async def get_id(message: Message):
    await message.answer(text=message.chat.id)
