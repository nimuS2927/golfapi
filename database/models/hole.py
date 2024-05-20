from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base

if TYPE_CHECKING:
    from .tournaments import Tournament


class Hole(Base):
    number: Mapped[int]
    par: Mapped[int]
    difficulty: Mapped[int]
    tournaments: Mapped[List['Tournament']] = relationship(
        back_populates='holes',
        secondary=tournament_flight_association_table,
    )