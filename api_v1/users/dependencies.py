from typing import Annotated, List
from fastapi import Path, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.schemas import UserId
from api_v1.common_crud import crud as crud_common
from api_v1.users import crud
from database import models
from database.helper_for_db import db_helper


async def user_by_id(
        user_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.User:
    user = await crud_common.read_obj(
        session=session,
        obj_id=user_id,
        obj=models.User,
    )
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found"
    )


async def user_by_tg_id(
        user_tg_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.User:
    user = await crud.get_user_by_tg_id(session, user_tg_id)
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_tg_id} not found"
    )


async def user_by_tg_id_body(
        user_tg_id: Annotated[UserId, Body],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.User:
    user = await crud.get_user_by_tg_id(session, user_tg_id.user_tg_id)
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_tg_id.user_tg_id} not found"
    )


async def users_all(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> List[models.User]:
    users = await crud_common.read_objs(session, models.User)
    if users:
        return users

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Users not found"
    )