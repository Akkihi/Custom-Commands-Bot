from aiogram.types import Message

from auth import dp


@dp.message_handler(commands=['start'])
async def start(message: Message):
    pass
