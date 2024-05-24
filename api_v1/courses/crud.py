from datetime import datetime
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from database.models import Course


async def get_course_by_name(
    session: AsyncSession,
    name: str
) -> Optional[Course]:
    stmt = select(Course).where(Course.name == name)
    result: Result = await session.execute(stmt)
    course = result.scalar()
    return course

