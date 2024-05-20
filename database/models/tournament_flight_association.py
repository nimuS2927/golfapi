from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint

from .base import Base


tournament_flight_association_table = Table(
    "tournament_flight_association",
    Base.metadata,
    Column("tournament_id", ForeignKey('tournaments.id'), nullable=False),
    Column("flight_id", ForeignKey('flights.id'), nullable=False),
    UniqueConstraint("tournament_id", "flight_id", name="idx_unique_tournament_flight")
)

