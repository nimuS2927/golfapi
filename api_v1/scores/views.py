from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.helper_for_db import db_helper
from database import models

from api_v1.common_crud import crud as crud_common
from api_v1.scores.dependencies import (
    score_by_id,
    score_by_id_tournament,
    score_by_id_tournament_and_id_hole,
    score_by_id_tournament_and_id_user,
    scores_all)
from api_v1.scores import schemas
from api_v1.scores.schemas import (
    CreateScore,
    UpdateScore,
    UpdateScorePartial,
)


router = APIRouter(prefix='/score', tags=['Scores'])


@router.get('/', response_model=List[schemas.Score])
async def get_scores(
        scores: List[models.Score] = Depends(scores_all),
) -> List[models.Score]:
    return scores


@router.get('/{score_id}/', response_model=schemas.Score)
async def get_score_by_id(
        score: models.Score = Depends(score_by_id),
) -> models.Score:
    return score


@router.get('/{id_tournament}/hole/{id_hole}', response_model=List[schemas.Score])
async def get_score_by_id_tournament_and_id_hole(
        scores: models.Score = Depends(score_by_id_tournament_and_id_hole),
) -> List[models.Score]:
    return scores


@router.get('/{id_tournament}/user/{id_user}', response_model=List[schemas.Score])
async def get_score_by_id_tournament_and_id_user(
        scores: models.Score = Depends(score_by_id_tournament_and_id_user),
) -> List[models.Score]:
    return scores


@router.get('/{id_tournament}/', response_model=List[schemas.Score])
async def get_score_by_id_tournament(
        scores: models.Score = Depends(score_by_id_tournament),
) -> List[models.Score]:
    return scores


@router.post(
    '/',
    response_model=schemas.Score,
    status_code=status.HTTP_201_CREATED
)
async def create_score(
    score_in: CreateScore,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Score:
    return await crud_common.create_obj(
        session=session,
        obj_in=score_in,
        obj=models.Score
    )


@router.put('/{score_id}/', response_model=schemas.Score)
async def update_score(
    score_update: UpdateScore,
    score: models.Score = Depends(score_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Score:
    return await crud_common.update_obj(
        session=session,
        obj=score,
        obj_update=score_update,
    )


@router.patch('/{score_id}/', response_model=schemas.Score)
async def update_score_partial(
    score_update: UpdateScorePartial,
    score: models.Score = Depends(score_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Score:
    return await crud_common.update_obj(
        session=session,
        obj=score,
        obj_update=score_update,
        partial=True,
    )


@router.delete(
    '/{score_id}/',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_score(
        score: models.Score = Depends(score_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud_common.delete_obj(
        session=session,
        obj=score
    )
