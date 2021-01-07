from aiogram.types import Message, ParseMode
from auth import dp
from utils import logger


@dp.message_handler(commands=['start', 'help'])
@logger.log_msg
async def start(message: Message):
    await message.answer(text="Привет! icmdbot - это бот для твоих кастомных команд под рукой!"
                         "\n**Доступные команды:**"
                         "\n /add (название команды)[в ответ на сообщение] — создать команду"                        
                         "\n /addr (название команды) [в ответ на сообщение] — создать reply команду"
                         "\n /del (название команды) - удаляет созданную команду"
                         "\n /help или /start - выводит это же сообщение", parse_mode=ParseMode.MARKDOWN)
