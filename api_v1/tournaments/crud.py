from datetime import datetime
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from database.models import Tournament


async def get_tournament_by_name(
    session: AsyncSession,
    name: str
) -> Optional[Tournament]:
    stmt = select(Tournament).where(Tournament.name == name)
    result: Result = await session.execute(stmt)
    user = result.scalar()
    return user


async def get_tournament_ge_start_and_le_end(
    session: AsyncSession,
    start: datetime,
    end: Optional[datetime],
) -> Optional[List[Tournament]]:
    if not end:
        stmt = select(Tournament).where(Tournament.start >= start).order_by(Tournament.start)
    else:
        stmt = select(Tournament).where(Tournament.start >= start, Tournament.end <= end).order_by(Tournament.start)
    result: Result = await session.execute(stmt)
    tournaments = result.scalars().all()
    return list(tournaments)
