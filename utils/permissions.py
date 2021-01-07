from datetime import datetime
from typing import Union

import config
import models


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
