import os
from aiogram.types import Message, ContentType
import asyncio

from aiogram.utils.exceptions import BadRequest

import config
from auth import dp
from services.pinterest import pinterest
from services.vk import vk
from utils import permissions, download


@dp.message_handler(lambda msg: permissions.is_admin(msg.from_user.username)
                                and not msg.media_group_id,
                    content_types=[ContentType.PHOTO,
                                   ContentType.VIDEO,
                                   ContentType.AUDIO,
                                   ContentType.STICKER,
                                   ContentType.DOCUMENT,
                                   ContentType.ANIMATION
                                   ])
async def on_media(message: Message):
    print("Отправляется одна картинка.")
    await message.copy_to(config.target_channel_id)

    try:
        file_path = await download.download_media(message.photo or
                                                  message.document or
                                                  message.audio or
                                                  message.video or
                                                  message.sticker)
    except BadRequest as e:
        await message.reply('Произошла ошибка получения файла, попробуйте еще раз')
        return

    # тут рассылка на другие сервисы
    await vk.wall_upload(file_path, message.caption)
    pinterest.handle_media(file_path, message.caption)

    await message.answer('Cообщение отослано.')
    await asyncio.sleep(1)
