from peewee import *

from .base_model import BaseModel
from .chat import Chat
from .tarif_type import TarifType


class ChatTarif(BaseModel):
    chat = ForeignKeyField(Chat, backref='tarif', null=False, unique=True)
    tarif_type = ForeignKeyField(TarifType, null=False)
    custom_limit = IntegerField(null=True)
    to_date = DateTimeField(null=True)
