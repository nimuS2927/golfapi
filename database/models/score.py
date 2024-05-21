from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Text, Numeric, ForeignKey

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base
from .tournament_hole_association import tournament_hole_association_table

if TYPE_CHECKING:
    from .tournaments import Tournament
    from .hole import Hole
    from .user import User
    from .flights import Flight


class Score(Base):
    id_tournament: Mapped[int] = mapped_column(ForeignKey('tournaments.id', ondelete='RESTRICT'))
    id_hole: Mapped[Optional[int]] = mapped_column(ForeignKey('holes.id', ondelete='SET NULL'))
    id_user: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'))
    id_flight: Mapped[Optional[int]] = mapped_column(ForeignKey('flights.id', ondelete='SET NULL'))
    id_total_score: Mapped[Optional[int]] = mapped_column(ForeignKey('totalscores.id', ondelete='RESTRICT'))
    impacts: Mapped[Optional[int]]
    tournament: Mapped['Tournament'] = relationship(back_populates='scores')
    hole: Mapped['Hole'] = relationship(back_populates='scores')
    user: Mapped['User'] = relationship(back_populates='scores')
    flight: Mapped['Flight'] = relationship(back_populates='scores')
    totalscore: Mapped['TotalScore'] = relationship(back_populates='scores')


class TotalScore(Base):
    id_tournament: Mapped[int] = mapped_column(ForeignKey('tournaments.id', ondelete='RESTRICT'))
    id_user: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'))
    id_flight: Mapped[Optional[int]] = mapped_column(ForeignKey('flights.id', ondelete='SET NULL'))
    tournament: Mapped['Tournament'] = relationship(back_populates='scores')
    user: Mapped['User'] = relationship(back_populates='scores')
    flight: Mapped['Flight'] = relationship(back_populates='scores')
    scores: Mapped[List['Score']] = relationship(
        back_populates='totalscore'
    )
    total: Mapped[Optional[int]]
