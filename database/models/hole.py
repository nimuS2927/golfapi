from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import String, Text, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base

if TYPE_CHECKING:
    from .score import Score
    from .course import Course


class Hole(Base):
    number: Mapped[int]
    par: Mapped[int]
    difficulty: Mapped[int]
    id_course: Mapped[int] = mapped_column(ForeignKey('courses.id', ondelete="SET NULL"),)
    scores: Mapped[List['Score']] = relationship(back_populates='hole')
    course: Mapped['Course'] = relationship(back_populates='holes')
