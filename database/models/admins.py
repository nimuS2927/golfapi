from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models import Base


class Admin(Base):
    login: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[bytes]
