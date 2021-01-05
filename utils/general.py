from aiogram.types import User


def get_full_name(user: User):
    return (user.first_name or '') + ' ' + (user.last_name or '')
