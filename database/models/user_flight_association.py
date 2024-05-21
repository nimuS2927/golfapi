from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint

from .base import Base


user_flight_association_table = Table(
    "user_flight_association",
    Base.metadata,
    Column("user_id", ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
    Column("flight_id", ForeignKey('flights.id', ondelete='CASCADE'), nullable=False),
    UniqueConstraint("user_id", "flight_id", name="idx_unique_user_flight")
)

