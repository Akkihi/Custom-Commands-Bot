import models
from aiogram.types import Message, ChatType, Chat, Update
from auth import dp
import config

channel_id = config.target_channel_id


@dp.message_handler(commands='add', chat_type=ChatType.PRIVATE)
async def add_command(message: Message):
    result = await message.reply_to_message.copy_to(chat_id=channel_id)
    print(result)
    #models.save_user(Message.from_user)
    models.save_command(trigger=message.reply_to_message.text, text=result.text,
                        media=result.document or result.photo[-1] or result.audio,
                        created_by=message.from_user.id)
    await message.reply(text='Команда добавлена.')


@dp.message_handler(commands='addr', chat_type=ChatType.GROUP)
async def add_command_reply(message: Message):
    result = await message.reply_to_message.copy_to(chat_id=channel_id)
    print(result)
    # models.save_user(Message.from_user)
    models.save_command(trigger=message.reply_to_message.text, text=result.text,
                        media=result.document or result.photo[-1] or result.audio,
                        created_by=message.from_user.id)
    await message.reply(text='Команда добавлена.')


@dp.message_handler(commands='del', chat_type=ChatType.GROUP)
async def delete_command(message: Message):
    await message.reply(text='Команда удалена.')
