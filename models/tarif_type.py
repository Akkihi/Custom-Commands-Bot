from peewee import *

from .base_model import BaseModel


class TarifType(BaseModel):
    name = TextField(unique=True, null=False)
    default_limit = IntegerField(null=True)
