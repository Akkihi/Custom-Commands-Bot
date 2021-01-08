from aiogram.dispatcher.handler import SkipHandler
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InlineQueryResultPhoto, \
    InlineQueryResultDocument, \
    InlineQueryResultVideo, InlineQueryResultVoice, InlineQueryResultGif, InputTextMessageContent, ParseMode

from auth import dp
from models import save_chat, save_user, Command, Chat, User
from utils.general import get_full_name_link


@dp.message_handler(lambda msg: msg.is_command())
async def on_trigger(message: Message):
    trigger = message.get_command()[1:]
    db_user, created = save_user(message.from_user)
    db_chat, created = save_chat(message.chat)
    chat_id = message.chat.id

    try:
        command = Command.get((Command.created_by == db_user)
                              & (Command.to_chat == db_chat)
                              & (Command.is_inline == False)
                              & (Command.trigger == trigger))
    except Exception as e:
        print(e)
        raise SkipHandler

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
    except Exception as e:
        item = InlineQueryResultArticle(id='0', title='Вы можете добавить комманды',
                                        input_message_content=InputTextMessageContent(
                                            'Вы можете доабаить комманды в бота @icmd_bot',
                                            parse_mode=ParseMode.HTML))
        try:
            await inline_query.bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)
        except Exception as e:
            print(e)
            return
        return

    db_target_user = None
    if '@' in trigger:  # todo сделать проверку при сохранении на наличие собачки
        target_username = None
        parts = trigger.split()
        parts.reverse()
        for part in parts:
            if part.startswith('@'):
                if len(part) < 6:
                    continue
                target_username = part[1:]
                trigger = trigger.replace(' ' + part, '')
                break
        try:
            db_target_user = User.get(User.username == target_username)
        except Exception as e:
            print(e)
            return  # todo вывод ошибки

    try:
        command = Command.get((Command.created_by == db_user)
                              & (Command.to_chat == db_chat)
                              & (Command.is_inline == True)
                              & (Command.trigger == trigger))
    except Exception as e:
        commands = Command.select().where((Command.created_by == db_user)
                                          & (Command.to_chat == db_chat)
                                          & (Command.is_inline == True))
        items = []
        if len(commands) > 0:
            for command in commands:
                if command.text:
                    if db_target_user and command.is_reply:
                        caption = get_full_name_link(
                            inline_query.from_user) + ' ' + command.text + ' ' + get_full_name_link(
                            db_target_user)
                    else:
                        caption = command.text
                else:
                    caption = None
                item_id = str(len(items))
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

        else:
            item = InlineQueryResultArticle(id='0', title='Вы можете добавить комманды',
                                            input_message_content=InputTextMessageContent(
                                                'Вы можете доабаить комманды в бота @icmd_bot',
                                                parse_mode=ParseMode.HTML))
            items.append(item)
        try:
            await inline_query.bot.answer_inline_query(inline_query.id, results=items, cache_time=1)
        except Exception as e:
            print(e)
            return
        return

    if command.text:
        if db_target_user and command.is_reply:
            caption = get_full_name_link(inline_query.from_user) + ' ' + command.text + ' ' + get_full_name_link(
                db_target_user)
        else:
            caption = command.text
    else:
        caption = None

    if command.media_type == 'photo':
        item = InlineQueryResultPhoto(id='0', photo_url=command.media_file_id, thumb_url=command.media_file_id,
                                      caption=caption, parse_mode=ParseMode.HTML)
    elif command.media_type == 'document' or command.media_type == 'audio':
        item = InlineQueryResultDocument(id='0', document_url=command.media_file_id, thumb_url=command.media_file_id,
                                         title='document', mime_type='application/zip', caption=caption,
                                         parse_mode=ParseMode.HTML)
    elif command.media_type == 'animation':
        item = InlineQueryResultGif(id='0', gif_url=command.media_file_id, thumb_url=command.media_file_id, title='gif',
                                    caption=caption, parse_mode=ParseMode.HTML)
    elif command.media_type == 'voice':
        item = InlineQueryResultVoice(id='0', voice_url=command.media_file_id, caption=caption, title='voice',
                                      parse_mode=ParseMode.HTML)
    elif command.media_type == 'video':
        item = InlineQueryResultVideo(id='0', video_url=command.media_file_id, thumb_url=command.media_file_id,
                                      caption=caption, title='video', mime_type='video/mp4', parse_mode=ParseMode.HTML)
    else:
        item = InlineQueryResultArticle(id='0', title='текст', input_message_content=InputTextMessageContent(caption,
                                                                                                             parse_mode=ParseMode.HTML))

    try:
        await inline_query.bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)
    except Exception as e:
        print(e)
        return
