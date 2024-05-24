from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Text, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base

if TYPE_CHECKING:
    from .hole import Hole
    from .tournaments import Tournament


class Course(Base):
    name: Mapped[str]
    holes: Mapped[List['Hole']] = relationship(back_populates='course')
    tournaments: Mapped[List['Tournament']] = relationship(
        back_populates='course',
    )
