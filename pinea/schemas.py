from datetime import date, datetime
from pydantic import BaseModel, ConfigDict

from pinea.models import OS, Entregue


class Token(BaseModel):
    access_token: str
    token_type: str

class EntregueUpdate(BaseModel):
    entregue: Entregue

class Message(BaseModel):
    message: str

class OSSchema(BaseModel):
    cliente: str
    entrega: str
    telefone: str

class OSPublica(BaseModel):
    id: int
    cliente: str
    entrega: str
    telefone: str
    entregue: Entregue

    model_config = ConfigDict(from_attributes=True)

class OSList(BaseModel):
    os: list[OSPublica]

