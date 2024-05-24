from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base

if TYPE_CHECKING:
    from .score import Score


class Hole(Base):
    number: Mapped[int]
    par: Mapped[int]
    difficulty: Mapped[int]
    scores: Mapped[List['Score']] = relationship(
        back_populates='hole',
    )
