from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.common_crud import crud as crud_common
from api_v1.holes import crud
from database import models
from database.helper_for_db import db_helper


async def hole_by_id(
        hole_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Hole:
    hole = await crud_common.read_obj(
        session=session,
        obj_id=hole_id,
        obj=models.Hole,
    )
    if hole:
        return hole

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Hole {hole_id} not found"
    )


async def hole_by_number(
        number: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Hole:
    hole = await crud.get_hole_by_number(session, number)
    if hole:
        return hole

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Hole {number} not found"
    )


async def holes_all(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Hole:
    holes = await crud_common.read_objs(session, models.Hole)
    if holes:
        return holes

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Holes not found"
    )