from datetime import datetime
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from database.models import TotalScore


async def get_totalscore_by_id_tournament(
    session: AsyncSession,
    id_tournament: int
) -> Optional[List[TotalScore]]:
    stmt = select(TotalScore).where(TotalScore.id_tournament == id_tournament)
    result: Result = await session.execute(stmt)
    totalscores = result.scalars().all()
    if totalscores:
        return list(totalscores)
    return None


async def get_totalscore_by_id_tournament_and_id_user(
    session: AsyncSession,
    id_tournament: int,
    id_user: int,
) -> Optional[TotalScore]:
    stmt = select(TotalScore).where(
        TotalScore.id_tournament == id_tournament,
        TotalScore.id_user == id_user
    )
    result: Result = await session.execute(stmt)
    score = result.scalar()
    if score:
        return score
    return None
