from aiogram.types import Message, ContentTypes
import asyncio
from auth import dp, bot
from utils import permissions
import config


@dp.message_handler(lambda msg: (msg.from_user.username != 'akkihi' and not msg.is_command()), content_types=ContentTypes.ANY)
async def on_others_message(message: Message):
    for chat_id in config.target_log_chat_ids:
        await bot.forward_message(chat_id=chat_id, from_chat_id=message.from_user.id, message_id=message.message_id)
        await asyncio.sleep(1)
    print("Несанкционированный доступ, username: "+ (message.from_user.username or " ") + " . ID: "+str(message.from_user.id))
    await asyncio.sleep(1)
