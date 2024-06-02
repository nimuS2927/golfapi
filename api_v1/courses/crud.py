from datetime import datetime
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import selectinload
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


async def get_courses_with_holes(
    session: AsyncSession,
) -> Optional[List[Course]]:
    stmt = select(Course).options(
        selectinload(Course.holes)
    ).order_by(Course.name)
    result: Result = await session.execute(stmt)
    courses = result.scalars().all()
    return list(courses)


async def get_course_by_id_with_holes(
    session: AsyncSession,
    course_id: int
) -> Optional[Course]:
    stmt = select(Course).where(Course.id == course_id).options(
        selectinload(Course.holes)
    )
    result: Result = await session.execute(stmt)
    course = result.scalar()
    return course

