from typing import List

from aiogram.dispatcher.handler import SkipHandler
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InlineQueryResultPhoto, \
    InlineQueryResultDocument, \
    InlineQueryResultVideo, InlineQueryResultVoice, InlineQueryResultGif, InputTextMessageContent, ParseMode, \
    InlineQueryResult

from auth import dp
from models import save_chat, save_user, Command, Chat, User
from utils.general import get_full_name_link


@dp.message_handler(lambda msg: msg.is_command())
async def on_trigger(message: Message):
    trigger = message.get_command(pure=True)
    for part in message.text.split(' ')[1:]:
        trigger += ' ' + part
    db_user, created = save_user(message.from_user)
    db_chat, created = save_chat(message.chat)
    chat_id = message.chat.id

    try:
        command = Command.get((Command.to_chat == db_chat)
                              & (Command.is_inline == False)
                              & (Command.trigger == trigger))
    except Exception as e:
        print(e)
        raise SkipHandler  # скипаем хендлер чтобы если это не триггер а комманда бота то она была обработана

    if command.is_reply and not message.reply_to_message:
        await message.answer('Комманда должна быть отправлена ответом на сообщение')
        return

    try:
        await message.delete()
    except:
        pass

    if command.text:
        caption = command.text
        if command.is_reply:
            caption = get_full_name_link(message.from_user) + ' ' + command.text + ' ' + get_full_name_link(
                message.reply_to_message.from_user)
    else:
        caption = None

    if command.media_type == 'photo':
        await message.bot.send_photo(chat_id=chat_id, photo=command.media_file_id, caption=caption,
                                     parse_mode=ParseMode.HTML)
    if command.media_type == 'document':
        await message.bot.send_document(chat_id=chat_id, document=command.media_file_id, caption=caption,
                                        parse_mode=ParseMode.HTML)
    if command.media_type == 'audio':
        await message.bot.send_audio(chat_id=chat_id, audio=command.media_file_id, caption=caption, title='audio',
                                     parse_mode=ParseMode.HTML)
    if command.media_type == 'video':
        await message.bot.send_video(chat_id=chat_id, video=command.media_file_id, caption=caption,
                                     parse_mode=ParseMode.HTML)
    if command.media_type == 'sticker':
        await message.bot.send_sticker(chat_id=chat_id, sticker=command.media_file_id)
    if command.media_type == 'voice':
        await message.bot.send_voice(chat_id=chat_id, voice=command.media_file_id, caption=caption,
                                     parse_mode=ParseMode.HTML)
    if command.media_type == 'animation':
        await message.bot.send_animation(chat_id=chat_id, animation=command.media_file_id, caption=caption,
                                         parse_mode=ParseMode.HTML)
    if command.media_type == 'video_note':
        await message.bot.send_video_note(chat_id=chat_id, video_note=command.media_file_id)
    if command.media_type == 'no_media':
        await message.bot.send_message(chat_id=chat_id, text=caption, parse_mode=ParseMode.HTML)


@dp.inline_handler()
async def on_inline_trigger(inline_query: InlineQuery):
    trigger = inline_query.query
    db_user, created = save_user(inline_query.from_user)
    try:
        db_chat = Chat.get(Chat.telegram_id == db_user.telegram_id)
    except Exception as e:  # если юзер который вызывает комманду не найден в базе
        items = InlineQueryResultArticle(id='0', title='Вы можете добавить комманды',
                                         input_message_content=InputTextMessageContent(
                                            'Вы можете доабаить комманды в бота @icmdbot',
                                            parse_mode=ParseMode.HTML))

        await inline_query.bot.answer_inline_query(inline_query.id, results=[items], cache_time=1,
                                                  switch_pm_text="Нажми, чтобы перейти в бота",
                                                   switch_pm_parameter='start')
        return

    # проверяем если в запросе есть собачка значит там юзернейм пользователя и пытаемся его найти
    db_target_user = None
    if '@' in trigger:
        target_username = None
        parts = trigger.split()
        parts.reverse()         # инвертируем массив для того чтобы брать последний указанный юзернейм
        for part in parts:
            if part.startswith('@'):
                if len(part) < 6:
                    continue
                target_username = part[1:]
                trigger = trigger.replace(' ' + part, '') # вырезаем юзернейм из комманды чтобы потом искать ее в базе
                break
        try:
            db_target_user = User.get(User.username == target_username)
        except Exception as e:  # если юзер которого указали в запросе не найден то не делаем ничего и не отправляем комманду
            return  # todo вывод ошибки

    try:
        commands = Command.select().where((Command.created_by == db_user)
                                          & (Command.to_chat == db_chat)
                                          & (Command.is_inline == True)
                                          & (Command.trigger.startswith(trigger)))
    except Exception as e:  # если комманда не найдена то выводим весь список комманд
        commands = Command.select().where((Command.created_by == db_user)
                                          & (Command.to_chat == db_chat)
                                          & (Command.is_inline == True))

    items = get_inline_query_result(commands, db_target_user) # здесь одну комманду оборачиваем в массив потому что фунцкия принимает массивы

    await inline_query.bot.answer_inline_query(inline_query.id, results=items, cache_time=1,
                                               switch_pm_text='Перейти в бота', switch_pm_parameter='0')


def get_inline_query_result(commands: List[Command], target_user: User = None) -> List[InlineQueryResult]:
    items = []
    if len(commands) > 0:
        for command in commands:

            if command.text:
                if target_user and command.is_reply:
                    caption = get_full_name_link(command.created_by) + ' ' + command.text + ' ' + get_full_name_link(
                        target_user)
                elif command.is_reply:
                    caption = get_full_name_link(command.created_by) + ' ' + command.text
                else:
                    caption = command.text
            else:
                caption = None

            item_id = str(len(items)) # айдишник текущего варианта будет равен длине массива уже созданных варикантов

            if command.media_type == 'photo':
                item = InlineQueryResultPhoto(id=item_id, photo_url=command.media_file_id,
                                              thumb_url=command.media_file_id,
                                              caption=caption, parse_mode=ParseMode.HTML, title=command.trigger)
            elif command.media_type == 'document' or command.media_type == 'audio':
                item = InlineQueryResultDocument(id=item_id, document_url=command.media_file_id,
                                                 thumb_url=command.media_file_id,
                                                 title=command.trigger, mime_type='application/zip',
                                                 caption=caption,
                                                 parse_mode=ParseMode.HTML)
            elif command.media_type == 'animation':
                item = InlineQueryResultGif(id=item_id, gif_url=command.media_file_id,
                                            thumb_url=command.media_file_id, title=command.trigger,
                                            caption=caption, parse_mode=ParseMode.HTML)
            elif command.media_type == 'voice':
                item = InlineQueryResultVoice(id=item_id, voice_url=command.media_file_id, caption=caption,
                                              title=command.trigger,
                                              parse_mode=ParseMode.HTML)
            elif command.media_type == 'video':
                item = InlineQueryResultVideo(id=item_id, video_url=command.media_file_id,
                                              thumb_url=command.media_file_id,
                                              caption=caption, title=command.trigger, mime_type='video/mp4',
                                              parse_mode=ParseMode.HTML)
            else:
                item = InlineQueryResultArticle(id=item_id, title=command.trigger,
                                                input_message_content=InputTextMessageContent(caption,
                                                                                              parse_mode=ParseMode.HTML))
            items.append(item)

    else:   # если комманд нету то выводим приглашение
        item = InlineQueryResultArticle(id='0', title='Комманд нету',
                                        input_message_content=InputTextMessageContent(
                                            'Вы можете доабаить комманды в бота @icmdbot',
                                            parse_mode=ParseMode.HTML))
        items.append(item)

    return items
