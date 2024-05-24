from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.helper_for_db import db_helper
from database import models

from api_v1.common_crud import crud as crud_common
from api_v1.totalscores.dependencies import (
    totalscore_by_id,
    totalscore_by_id_tournament,
    totalscore_by_id_tournament_and_id_user,
    totalscores_all)
from api_v1.totalscores import schemas
from api_v1.totalscores.schemas import (
    CreateTotalScore,
    UpdateTotalScore,
    UpdateTotalScorePartial,
)


router = APIRouter(prefix='/totalscore', tags=['TotalScores'])


@router.get('/', response_model=List[schemas.TotalScore])
async def get_totalscores(
        totalscores: List[models.TotalScore] = Depends(totalscores_all),
) -> List[models.TotalScore]:
    return totalscores


@router.get('/{totalscore_id}/', response_model=schemas.TotalScore)
async def get_totalscore_by_id(
        totalscore: models.TotalScore = Depends(totalscore_by_id),
) -> models.TotalScore:
    return totalscore


@router.get('/{id_tournament}/user/{id_user}', response_model=List[schemas.TotalScore])
async def get_totalscore_by_id_tournament_and_id_user(
        totalscore: models.TotalScore = Depends(totalscore_by_id_tournament_and_id_user),
) -> models.TotalScore:
    return totalscore


@router.get('/{id_tournament}/', response_model=List[schemas.TotalScore])
async def get_totalscore_by_id_tournament(
        totalscores: models.TotalScore = Depends(totalscore_by_id_tournament),
) -> List[models.TotalScore]:
    return totalscores


@router.post(
    '/',
    response_model=schemas.TotalScore,
    status_code=status.HTTP_201_CREATED
)
async def create_totalscore(
    totalscore_in: CreateTotalScore,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.TotalScore:
    return await crud_common.create_obj(
        session=session,
        obj_in=totalscore_in,
        obj=models.TotalScore
    )


@router.put('/{totalscore_id}/', response_model=schemas.TotalScore)
async def update_totalscore(
    totalscore_update: UpdateTotalScore,
    totalscore: models.TotalScore = Depends(totalscore_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.TotalScore:
    return await crud_common.update_obj(
        session=session,
        obj=totalscore,
        obj_update=totalscore_update,
    )


@router.patch('/{totalscore_id}/', response_model=schemas.TotalScore)
async def update_totalscore_partial(
    totalscore_update: UpdateTotalScorePartial,
    totalscore: models.TotalScore = Depends(totalscore_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.TotalScore:
    return await crud_common.update_obj(
        session=session,
        obj=totalscore,
        obj_update=totalscore_update,
        partial=True,
    )


@router.delete(
    '/{totalscore_id}/',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_totalscore(
        totalscore: models.TotalScore = Depends(totalscore_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud_common.delete_obj(
        session=session,
        obj=totalscore
    )
