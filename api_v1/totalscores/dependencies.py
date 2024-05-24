from typing import Annotated, List, Optional
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.common_crud import crud as crud_common
from api_v1.totalscores import crud
from database import models
from database.helper_for_db import db_helper


async def totalscore_by_id(
        totalscore_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.TotalScore:
    totalscore = await crud_common.read_obj(
        session=session,
        obj_id=totalscore_id,
        obj=models.TotalScore,
    )
    if totalscore:
        return totalscore

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"TotalScore {totalscore_id} not found"
    )


async def totalscore_by_id_tournament(
        id_tournament: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> List[models.TotalScore]:
    totalscores = await crud.get_totalscore_by_id_tournament(session, id_tournament)
    if totalscores:
        return totalscores

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"TotalScores {id_tournament} not found"
    )


async def totalscore_by_id_tournament_and_id_user(
        id_tournament: Annotated[int, Path],
        id_user: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.TotalScore:
    totalscores = await crud.get_totalscore_by_id_tournament_and_id_user(
        session=session,
        id_tournament=id_tournament,
        id_user=id_user
    )
    if totalscores:
        return totalscores

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"TotalScores {id_tournament=} and {id_user=} not found"
    )


async def totalscores_all(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> List[models.TotalScore]:
    totalscores = await crud_common.read_objs(session, models.TotalScore)
    if totalscores:
        return totalscores

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"TotalScores not found"
    )
