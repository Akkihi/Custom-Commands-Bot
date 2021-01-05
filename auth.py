from aiogram import Bot, Dispatcher
from aiogram.utils.executor import Executor

import config
from services.vk import vk

config.load_config()

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

runner = Executor(dp, skip_updates=False)
# на случай если захочешь менять параметры в процессе работы бота, конфиг будет записываться при выключении

runner.on_startup(vk.login)
runner.on_shutdown(vk.shutdown)
runner.on_shutdown(config.write_config)
