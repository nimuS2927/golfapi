from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base
from database.models.user_flight_association import user_flight_association_table
from database.models.user_tournament_association import user_tournament_association_table

if TYPE_CHECKING:
    from .flights import Flight
    from .tournaments import Tournament


class User(Base):
    id_telegram: Mapped[int] = mapped_column(unique=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[Optional[str]] = mapped_column(String(50))
    handicap: Mapped[float]
    image_src: Mapped[Optional[str]]
    status: Mapped[bool]
    flights: Mapped[List['Flight']] = relationship(
        back_populates='users',
        secondary=user_flight_association_table,
    )
    tournaments: Mapped[List['Tournament']] = relationship(
        back_populates='users',
        secondary=user_tournament_association_table,
    )
