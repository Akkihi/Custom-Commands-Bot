import os
import shutil
from typing import List, Union, Tuple

from aiogram.types import PhotoSize, Document, Animation, Sticker, Audio, Video
from aiogram.utils.exceptions import BadRequest

media_dir = 'media'

if not os.path.exists(media_dir):
    os.mkdir(media_dir)


async def download_media(media: Union[List[PhotoSize], Document, Animation, Sticker, Audio, Video],
                         custom_file_name=None
                         ) -> str:
    if type(media) is list:
        media = media[-1]

    file_url = await media.get_url()
    file_ext = file_url.split('.')[-1]

    buffered_writer = None

    for try_count in range(0, 3):
        try:
            if custom_file_name:
                custom_file_name_path = media_dir + \
                                        os.path.sep + \
                                        str(custom_file_name) + \
                                        '.' + \
                                        file_ext
                buffered_writer = await media.download(custom_file_name_path)
            else:
                buffered_writer = await media.download()
            buffered_writer.close()
            break
        except BadRequest as e:
            if try_count == 2:
                raise e
            print(e)
    print(buffered_writer.name)
    return buffered_writer.name

