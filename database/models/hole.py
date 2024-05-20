from datetime import datetime
from typing import Optional, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base


class Hole(Base):
    number: Mapped[int]
    par: Mapped[int]
    difficulty: Mapped[int]
