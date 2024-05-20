from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from auth.admins.schemas import AdminBase, CreateAdmin, GetAdmin
from core.utils import hash_password
from database.models import Admin
from core import utils as password_utils


async def get_admin_by_login(
    session: AsyncSession,
    admin_in: GetAdmin
) -> Optional[Admin]:
    stmt = select(Admin).where(Admin.login == admin_in.login)
    result: Result = await session.execute(stmt)
    admin = result.scalar()
    try:
        if not password_utils.validate_password(
                password=admin_in.password,
                hashed_password=admin.password,
        ):
            return None
        else:
            return admin
    except Exception:
        return None


async def get_admin_by_login_for_superuser(
    session: AsyncSession,
    admin_login: int
) -> Optional[Admin]:
    stmt = select(Admin).where(Admin.login == admin_login)
    result: Result = await session.execute(stmt)
    admin = result.scalar()
    if admin:
        return admin
    return None


async def create_admin(
    session: AsyncSession,
    admin_in: CreateAdmin,
) -> Admin:
    obj_ = Admin(login=admin_in.login, password=hash_password(admin_in.password))
    session.add(obj_)
    await session.commit()
    return obj_

