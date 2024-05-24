from typing import Annotated, List, Optional
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.common_crud import crud as crud_common
from api_v1.scores import crud
from database import models
from database.helper_for_db import db_helper


async def score_by_id(
        score_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Score:
    score = await crud_common.read_obj(
        session=session,
        obj_id=score_id,
        obj=models.Score,
    )
    if score:
        return score

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Score {score_id} not found"
    )


async def score_by_id_tournament(
        id_tournament: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> List[models.Score]:
    scores = await crud.get_score_by_id_tournament(session, id_tournament)
    if scores:
        return scores

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Scores {id_tournament} not found"
    )


async def score_by_id_tournament_and_id_hole(
        id_tournament: Annotated[int, Path],
        id_hole: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> List[models.Score]:
    scores = await crud.get_score_by_id_tournament_and_id_hole(
        session=session,
        id_tournament=id_tournament,
        id_hole=id_hole
    )
    if scores:
        return scores

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Scores {id_tournament=} and {id_hole=} not found"
    )


async def score_by_id_tournament_and_id_user(
        id_tournament: Annotated[int, Path],
        id_user: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> List[models.Score]:
    scores = await crud.get_score_by_id_tournament_and_id_user(
        session=session,
        id_tournament=id_tournament,
        id_user=id_user
    )
    if scores:
        return scores

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Scores {id_tournament=} and {id_user=} not found"
    )


async def scores_all(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> List[models.Score]:
    scores = await crud_common.read_objs(session, models.Score)
    if scores:
        return scores

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Scores not found"
    )
