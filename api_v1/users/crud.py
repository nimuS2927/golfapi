from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from database.models import User


async def get_user_by_tg_id(
    session: AsyncSession,
    tg_id: int
) -> Optional[User]:
    stmt = select(User).where(User.id_telegram == tg_id)
    result: Result = await session.execute(stmt)
    user = result.scalar()
    return user
