from typing import Optional

from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column

from database.models import Base


class User(Base):
    id_telegram: Mapped[int] = mapped_column(unique=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[Optional[str]] = mapped_column(String(50))
    handicap: Mapped[float]
