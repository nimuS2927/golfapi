from typing import Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from api_v1.users.schemas import CreateUser, UpdateUser, UpdateUserPartial
from auth.admins.schemas import CreateAdmin
from database.models import User, Admin


OBJECTS = [User, Admin]
OBJ_CREATE = [
    CreateUser,
]
OBJ_UPDATE = [
    UpdateUser,
    UpdateUserPartial,
]


async def create_obj(
    session: AsyncSession,
    obj_in: Union[*OBJ_CREATE],
    obj: Union[*OBJECTS]
) -> Union[*OBJECTS]:
    obj_ = obj(**obj_in.model_dump())
    session.add(obj_)
    await session.commit()
    return obj_


async def read_obj(
    session: AsyncSession,
    obj_id: int,
    obj: Union[*OBJECTS]
) -> Optional[Union[*OBJECTS]]:
    return await session.get(obj, obj_id)


async def update_obj(
    session: AsyncSession,
    obj: Union[*OBJECTS],
    obj_update: Union[*OBJ_UPDATE],
    partial: bool = False,
) -> Union[*OBJECTS]:
    for name, value in obj_update.model_dump(exclude_unset=partial).items():
        setattr(obj, name, value)
    await session.commit()
    return obj


async def delete_obj(
    session: AsyncSession,
    obj: Union[*OBJECTS],
) -> None:
    await session.delete(obj)
    await session.commit()
