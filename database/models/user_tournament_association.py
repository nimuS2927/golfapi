from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint

from .base import Base


user_tournament_association_table = Table(
    "user_tournament_association",
    Base.metadata,
    Column("user_id", ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
    Column("tournament_id", ForeignKey('tournaments.id', ondelete='CASCADE'), nullable=False),
    UniqueConstraint("user_id", "tournament_id", name="idx_unique_user_tournament")
)

