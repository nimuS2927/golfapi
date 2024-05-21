from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.helper_for_db import db_helper
from database import models

from api_v1.common_crud import crud as crud_common
from api_v1.holes.dependencies import hole_by_id, hole_by_number, holes_all
from api_v1.holes import schemas
from api_v1.holes.schemas import (
    CreateHole,
    UpdateHole,
    UpdateHolePartial,
)


router = APIRouter(prefix='/hole', tags=['Holes'])


@router.get('/', response_model=List[schemas.Hole])
async def get_holes(
        holes: List[models.Hole] = Depends(holes_all),
) -> List[models.Hole]:
    return holes


@router.get('/{hole_id}/', response_model=schemas.Hole)
async def get_hole(
        hole: models.Hole = Depends(hole_by_id),
) -> models.Hole:
    return hole


@router.get('/{hole_number}/', response_model=schemas.Hole)
async def get_hole(
        hole: models.Hole = Depends(hole_by_number),
) -> models.Hole:
    return hole


@router.post(
    '/',
    response_model=schemas.Hole,
    status_code=status.HTTP_201_CREATED
)
async def create_hole(
    hole_in: CreateHole,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Hole:
    return await crud_common.create_obj(
        session=session,
        obj_in=hole_in,
        obj=models.Hole
    )


@router.put('/{hole_id}/', response_model=schemas.Hole)
async def update_hole(
    hole_update: UpdateHole,
    hole: models.Hole = Depends(hole_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Hole:
    return await crud_common.update_obj(
        session=session,
        obj=hole,
        obj_update=hole_update,
    )


@router.patch('/{hole_id}/', response_model=schemas.Hole)
async def update_hole_partial(
    hole_update: UpdateHolePartial,
    hole: models.Hole = Depends(hole_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Hole:
    return await crud_common.update_obj(
        session=session,
        obj=hole,
        obj_update=hole_update,
        partial=True,
    )


@router.delete(
    '/{hole_id}/',
    status_code=status.HTTP_204_NO_CONTENT
)
async def update_hole(
        hole: models.Hole = Depends(hole_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud_common.delete_obj(
        session=session,
        obj=hole
    )
