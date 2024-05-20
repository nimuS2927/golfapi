from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.helper_for_db import db_helper
from database import models

from api_v1.common_crud import crud as crud_common
from api_v1.users.dependencies import user_by_id, user_by_tg_id
from api_v1.users import schemas
from api_v1.users.schemas import (
    CreateUser,
    UpdateUser,
    UpdateUserPartial,
)


router = APIRouter(prefix='/user', tags=['Users'])


@router.get('/', response_model=List[schemas.User])
async def get_users(
        users: List[models.User] = Depends(user_by_id),
) -> List[models.User]:
    return users


@router.get('/{user_id}/', response_model=schemas.User)
async def get_user(
        user: models.User = Depends(user_by_id),
) -> models.User:
    return user


@router.get('/tg/{user_tg_id}/', response_model=schemas.User)
async def get_user(
        user: models.User = Depends(user_by_tg_id),
) -> models.User:
    return user


@router.post(
    '/',
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_in: CreateUser,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.User:
    return await crud_common.create_obj(
        session=session,
        obj_in=user_in,
        obj=models.User
    )


@router.put('/{user_id}/', response_model=schemas.User)
async def update_user(
    user_update: UpdateUser,
    user: models.User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.User:
    return await crud_common.update_obj(
        session=session,
        obj=user,
        obj_update=user_update,
    )


@router.patch('/{user_id}/', response_model=schemas.User)
async def update_user_partial(
    user_update: UpdateUserPartial,
    user: models.User = Depends(user_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.User:
    return await crud_common.update_obj(
        session=session,
        obj=user,
        obj_update=user_update,
        partial=True,
    )


@router.delete(
    '/{user_id}/',
    status_code=status.HTTP_204_NO_CONTENT
)
async def update_user(
        user: models.User = Depends(user_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud_common.delete_obj(
        session=session,
        obj=user
    )
