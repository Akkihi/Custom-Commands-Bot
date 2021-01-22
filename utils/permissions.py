from datetime import datetime
from typing import Union

import config
import models


# Старый вариант премиума где дата окончания находится в таблице пользователей - удалить
def has_premium(db_user_or_chat: Union[models.User, models.Chat]) -> bool:
    premium_to = db_user_or_chat.premium_to
    if premium_to.year > datetime.now().year:
        return True
    if premium_to.year == datetime.now().year \
        and premium_to.month > datetime.now().month:
        return True
    if premium_to.year == datetime.now().year \
        and premium_to.month == datetime.now().month \
        and premium_to.day >= datetime.now().day:
        return True

    return False


# Новый вариант где дата окончания находится в таблице user_tarif или chat_tarif
# По окончанию этой даты надо сменить тариф на базовый
def has_premium_by_tarif(user_or_chat_tarif: Union[models.UserTarif, models.ChatTarif]) -> bool:
    premium_to = user_or_chat_tarif.to_date
    if premium_to.year > datetime.now().year:
        return True
    if premium_to.year == datetime.now().year \
            and premium_to.month > datetime.now().month:
        return True
    if premium_to.year == datetime.now().year \
            and premium_to.month == datetime.now().month \
            and premium_to.day >= datetime.now().day:
        return True

    return False
