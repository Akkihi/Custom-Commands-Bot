import os

from aiogram import Bot, Dispatcher
from aiogram.utils.executor import Executor

import config

config.load_config()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

runner = Executor(dp, skip_updates=True)
# на случай если захочешь менять параметры в процессе работы бота, конфиг будет записываться при выключении

runner.on_shutdown(config.write_config)
