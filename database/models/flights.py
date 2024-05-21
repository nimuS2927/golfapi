from typing import TYPE_CHECKING
from datetime import datetime
from typing import Optional, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base
from .tournament_flight_association import tournament_flight_association_table
from .user_flight_association import user_flight_association_table

if TYPE_CHECKING:
    from .user import User
    from .tournaments import Tournament


class Flight(Base):
    users: Mapped[Optional[List['User']]] = relationship(
        back_populates='flights',
        secondary=user_flight_association_table,
    )
    tournaments: Mapped[Optional[List['Tournament']]] = relationship(
        back_populates='flights',
        secondary=tournament_flight_association_table,
    )

