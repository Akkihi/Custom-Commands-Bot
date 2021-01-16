import models
from aiogram.types import Message, ChatType
from auth import dp
from utils.general import save_message_to_storage_channel
from utils import logger


@dp.message_handler(commands=['add', 'addr'], chat_type=[ChatType.PRIVATE,
                                                         ChatType.GROUP,
                                                         ChatType.SUPERGROUP,
                                                         ChatType.CHANNEL])
@logger.log_msg
async def add_command(message: Message):
    target_message = message.reply_to_message
    if not target_message:
        await message.answer('Команда должна быть ответом на сообщение')
        return

    trigger = message.get_args()
    if not trigger:
        await message.answer('Триггер после комманды не указан')
        return

    if len(trigger.split(' ')) > 1:
        await message.answer('Триггер должен состоять из одного слова')

    text = target_message.text or target_message.caption or none

    is_reply = message.get_command(pure=True) == 'addr'

    is_command_inline = False

    if message.chat.type == ChatType.PRIVATE: # проверяем ограничения для инлайн комманд
        if '@' in trigger:
            await message.answer('Нельзя сохранять симовол @ в комманду')
        if message.sticker or message.video_note:
            await message.answer('Данный тип медиа не поддерживается')
            return
        is_command_inline = True
    media = None

    if target_message.photo \
            or target_message.document \
            or target_message.audio \
            or target_message.voice \
            or target_message.video \
            or target_message.video_note \
            or target_message.animation \
            or target_message.sticker:
        media_message = await save_message_to_storage_channel(message.reply_to_message)
        media = media_message.audio \
                or media_message.voice \
                or media_message.document \
                or media_message.photo \
                or media_message.video \
                or media_message.video_note \
                or media_message.animation \
                or media_message.sticker

    models.save_command(trigger=trigger,
                        text=text,
                        media=media,
                        created_by=message.from_user,
                        to_chat=message.chat,
                        is_inline=is_command_inline,
                        is_reply=is_reply)

    await message.reply(text='Команда добавлена.')


@dp.message_handler(commands='del', chat_type=[ChatType.PRIVATE,
                                               ChatType.GROUP,
                                               ChatType.SUPERGROUP,
                                               ChatType.CHANNEL])
@logger.log_msg
async def delete_command(message: Message):
    trigger = message.get_args()
    if not trigger:
        await message.answer('Триггер после комманды не указан')
        return
    try:
        models.delete_command(trigger=trigger, to_chat=message.chat)
        await message.reply(text='Команда удалена.')
    except:
        await message.reply(text='Такой комманды не существует')


@dp.message_handler(commands='mycom', chat_type=ChatType.PRIVATE)
async def my_commands(message: Message):
    result = models.get_mycommands(created_by=message.from_user)
    mycom = ''
    for command in result:
        mycom += '/' + command.trigger + ' '
    await message.answer(text='Вот список твоих команд:\n' + str(mycom))


@dp.message_handler(commands='mycom', chat_type=[ChatType.CHANNEL,
                                                 ChatType.GROUP,
                                                 ChatType.SUPERGROUP])
async def chat_commands(message: Message):
    result = models.get_chatcommands(to_chat=message.chat)
    mycom = ''
    for command in result:
        mycom += '/' + command.trigger + ' '
    await message.answer(text='Вот список команд чата:\n' + str(mycom))


@dp.message_handler(commands='get_id', chat_type=ChatType.GROUP)
async def get_id(message: Message):
    await message.answer(text=message.chat.id)
