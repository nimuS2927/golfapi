from typing import TYPE_CHECKING
from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base
from .tournament_flight_association import tournament_flight_association_table
from .user_tournament_association import user_tournament_association_table

if TYPE_CHECKING:
    from .user import User
    from .flights import Flight
    from .score import Score
    from .score import TotalScore


class Tournament(Base):
    name: Mapped[str] = mapped_column(String(300))
    max_flights: Mapped[int]
    start: Mapped[datetime]
    end: Mapped[Optional[datetime]]
    type: Mapped[str]
    status: Mapped[Optional[bool]] = mapped_column(default=False, server_default=None)
    hcp: Mapped[Optional[int]] = mapped_column(default=None, server_default=None)
    id_course: Mapped[Optional[int]] = mapped_column(ForeignKey('courses.id', ondelete="SET NULL"))
    flights: Mapped[List['Flight']] = relationship(
        back_populates='tournaments',
        secondary=tournament_flight_association_table,
    )
    users: Mapped[List['User']] = relationship(
        back_populates='tournaments',
        secondary=user_tournament_association_table,
    )
    scores: Mapped[List['Score']] = relationship(
        back_populates='tournament'
    )
    totalscores: Mapped[List['TotalScore']] = relationship(
        back_populates='tournament'
    )
