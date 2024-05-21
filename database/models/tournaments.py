from typing import TYPE_CHECKING
from datetime import datetime
from typing import Optional, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base
from .tournament_flight_association import tournament_flight_association_table
from .tournament_hole_association import tournament_hole_association_table
from .user_tournament_association import user_tournament_association_table

if TYPE_CHECKING:
    from .user import User
    from .hole import Hole
    from .flights import Flight


class Tournament(Base):
    name: Mapped[str] = mapped_column(String(300))
    max_flights: Mapped[int]
    start: Mapped[datetime]
    end: Mapped[Optional[datetime]]
    hcp: Mapped[Optional[int]] = mapped_column(default=None, server_default=None)
    flights: Mapped[List['Flight']] = relationship(
        back_populates='tournaments',
        secondary=tournament_flight_association_table,
    )
    holes: Mapped[List['Hole']] = relationship(
        back_populates='tournaments',
        secondary=tournament_hole_association_table,
    )
    users: Mapped[List['User']] = relationship(
        back_populates='tournaments',
        secondary=user_tournament_association_table,
    )
