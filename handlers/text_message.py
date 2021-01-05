from aiogram.types import Message
import asyncio
import config
from auth import dp
from utils import permissions
from services.vk import vk
from services.pinterest import pinterest


@dp.message_handler(lambda msg: permissions.is_admin(msg.from_user.username) and not msg.is_command())
async def on_text_message(message: Message):
    await message.copy_to(config.target_channel_id)
    # рассылка текстовых сообщений
    await vk.text_message(message.text)
    pinterest.handle_text(message.text)

    await message.answer('Текстовое сообщение отослано.')
    await asyncio.sleep(1)
