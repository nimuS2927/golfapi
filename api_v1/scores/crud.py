from datetime import datetime
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from database.models import Score


async def get_score_by_id_tournament(
    session: AsyncSession,
    id_tournament: int
) -> Optional[List[Score]]:
    stmt = select(Score).where(Score.id_tournament == id_tournament)
    result: Result = await session.execute(stmt)
    scores = result.scalars().all()
    if scores:
        return list(scores)
    return None


async def get_score_by_id_tournament_and_id_hole(
    session: AsyncSession,
    id_tournament: int,
    id_hole: int,
) -> Optional[List[Score]]:
    stmt = select(Score).where(
        Score.id_tournament == id_tournament,
        Score.id_hole == id_hole
    ).order_by(Score.id_hole)
    result: Result = await session.execute(stmt)
    scores = result.scalars().all()
    if scores:
        return list(scores)
    return None


async def get_score_by_id_tournament_and_id_user(
    session: AsyncSession,
    id_tournament: int,
    id_user: int,
) -> Optional[List[Score]]:
    stmt = select(Score).where(
        Score.id_tournament == id_tournament,
        Score.id_user == id_user
    ).order_by(Score.id_hole)
    result: Result = await session.execute(stmt)
    scores = result.scalars().all()
    if scores:
        return list(scores)
    return None
