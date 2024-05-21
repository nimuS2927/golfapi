from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint

from .base import Base


tournament_hole_association_table = Table(
    "tournament_hole_association_table",
    Base.metadata,
    Column("tournament_id", ForeignKey('tournaments.id', ondelete='CASCADE'), nullable=False),
    Column("hole_id", ForeignKey('holes.id', ondelete='CASCADE'), nullable=False),
    UniqueConstraint("tournament_id", "hole_id", name="idx_unique_tournament_hole")
)

