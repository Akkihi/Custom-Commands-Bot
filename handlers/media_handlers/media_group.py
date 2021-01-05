import json
import asyncio

from aiogram.types import Message, ContentType
from aiogram.utils.exceptions import BadRequest

from auth import dp, runner
from utils import permissions, download
from utils.data import data
from ..command_handlers.send_media_group import send_media_group


@dp.message_handler(lambda msg: permissions.is_admin(msg.from_user.username)
                                and msg.media_group_id,
                    content_types=[ContentType.PHOTO, ContentType.VIDEO])
async def on_media_group(message: Message):
    #print(json.dumps(json.loads(str(message)), indent=4, sort_keys=True))
    if message.media_group_id not in data.keys():
        data[message.media_group_id] = dict()
        data[message.media_group_id]['media'] = list()
        data[message.media_group_id]['text'] = None
        data[message.media_group_id]['schedule_task'] = None
        data[message.media_group_id]['has_error'] = False

    if data[message.media_group_id]['has_error']:
        print('Пропуск сообщения {} по причине ошибки в медиа-группе'.format(message.message_id))
        return

    custom_file_name = str(message.media_group_id) + '_' + str(message.message_id)

    try:
        file_path = await download.download_media(message.photo or message.video,
                                                                 custom_file_name=custom_file_name)
    except BadRequest as e:
        await message.reply('Произошла ошибка скачивания сообщения, попробуйте еще раз')
        data[message.media_group_id]['has_error'] = True
        return

    data[message.media_group_id]['media'].append(file_path)

    if data[message.media_group_id]['schedule_task']:
        data[message.media_group_id]['schedule_task'].cancel()
    task = runner.loop.call_later(20, asyncio.ensure_future, send_media_group(message))
    data[message.media_group_id]['schedule_task'] = task

    if message.caption and len(message.caption) > 0:
        data[message.media_group_id]['text'] = message.caption

    await asyncio.sleep(1)
