from typing import Annotated, Optional
from fastapi import Path, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.common_crud import crud as com_crud
from auth.admins import crud as auth_crud
from auth.admins.schemas import AdminBase, GetAdmin, SuperUser
from core import c_project, utils as password_utils
from database.models import Admin
from database.helper_for_db import db_helper


async def admin_by_id(
        admin_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Optional[Admin]:
    admin: Optional[Admin] = await session.get(Admin, admin_id)
    if admin:
        return admin

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Admin {admin_id} not found"
    )


async def admin_by_login_for_superuser(
        admin_login: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Optional[Admin]:
    admin = await auth_crud.get_admin_by_login_for_superuser(
        session=session,
        admin_login=admin_login,
    )
    if admin:
        return admin

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Invalid login",
    )


async def admin_by_login(
        login: str,
        password: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Optional[Admin]:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    admin_in = GetAdmin(login=login, password=password)
    admin = await auth_crud.get_admin_by_login(
        session=session,
        admin_in=admin_in
    )
    if admin:
        return admin
    raise unauthed_exc


async def validate_superuser(
        superuser_in: SuperUser,
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    if superuser_in.login != c_project.auth_jwt.superuser:
        raise unauthed_exc
    if not password_utils.validate_password(
            password=superuser_in.password,
            hashed_password=c_project.auth_jwt.password,
    ):
        raise unauthed_exc
    return True
