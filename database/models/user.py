from typing import Optional, List

from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base
from database.models.user_flight_association import user_flight_association_table


class User(Base):
    id_telegram: Mapped[int] = mapped_column(unique=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[Optional[str]] = mapped_column(String(50))
    handicap: Mapped[float]
    flights: Mapped[List['User']] = relationship(
        back_populates='users',
        secondary=user_flight_association_table,
    )
