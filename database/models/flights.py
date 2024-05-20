from typing import TYPE_CHECKING
from datetime import datetime
from typing import Optional, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base
from .user_flight_association import user_flight_association_table

if TYPE_CHECKING:
    from .user import User


class Flight(Base):
    users: Mapped[List['User']] = relationship(
        back_populates='flights',
        secondary=user_flight_association_table,
    )

