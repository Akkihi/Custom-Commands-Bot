from peewee import *

from .base_model import BaseModel
from .user import User
from .tarif_type import TarifType


class UserTarif(BaseModel):
    user = ForeignKeyField(User, backref='tarif', null=False, unique=True)  # unique для того чтобы можно было иметь один тариф на пользователя
    tarif_type = ForeignKeyField(TarifType, null=False)
    custom_limit = IntegerField(null=True)
    to_date = DateTimeField(null=True)
