from datetime import date, datetime
from enum import Enum
from sqlalchemy.orm import Mapped, registry, mapped_column
from sqlalchemy import  func

table_registry = registry()

class Entregue(str, Enum):
    sim = 'sim'
    nao = 'nao'

@table_registry.mapped_as_dataclass
class OS:
    __tablename__ = 'os'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    cliente: Mapped[str]
    entrega: Mapped[str]
    entregue: Mapped[Entregue]
    telefone: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
      init=False,
      onupdate=func.now(),
      nullable=True,
      server_default=func.now(),
    )