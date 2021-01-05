import logging
from functools import wraps

from loguru import logger

from utils.general import get_full_name

logger.add('logs.log')


def log_msg(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        message = args[0]
        output = 'from user: {}, to chat: {}, message: {}'.format(get_full_name(message.from_user),
                                                                  message.chat.title or '',
                                                                  message.text or '')
        logger.log(logging.INFO, output)
        return func(*args, **kwargs)
    return wrapper
