from datetime import datetime
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from database.models import Hole


async def get_hole_by_number(
    session: AsyncSession,
    number: int
) -> Optional[Hole]:
    stmt = select(Hole).where(Hole.number == number)
    result: Result = await session.execute(stmt)
    hole = result.scalar()
    return hole


async def get_holes_by_course_id(
    session: AsyncSession,
    id_course: int
) -> Optional[List[Hole]]:
    stmt = select(Hole).where(Hole.id_course == id_course)
    result: Result = await session.execute(stmt)
    holes = result.scalars().all()
    return list(holes)

