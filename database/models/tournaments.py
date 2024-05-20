from typing import TYPE_CHECKING
from datetime import datetime
from typing import Optional, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base
from .tournament_flight_association import tournament_flight_association_table

if TYPE_CHECKING:
    from .user import User
    from .hole import Hole


class Tournament(Base):
    name: Mapped[str] = mapped_column(String(300))
    max_flights: Mapped[int]
    start: Mapped[datetime]
    end: Mapped[Optional[datetime]]
    users: Mapped[List['User']] = relationship(
        back_populates='tournaments',
        secondary=tournament_flight_association_table,
    )
    holes: Mapped[List['User']] = relationship(
        back_populates='tournaments',
        secondary=tournament_flight_association_table,
    )
