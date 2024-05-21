from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.common_crud import crud as crud_common
from api_v1.tournaments import crud
from database import models
from database.helper_for_db import db_helper


async def tournament_by_id(
        tournament_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Tournament:
    tournament = await crud_common.read_obj(
        session=session,
        obj_id=tournament_id,
        obj=models.Tournament,
    )
    if tournament:
        return tournament

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tournament {tournament_id} not found"
    )


async def tournament_by_name(
        name: Annotated[str, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Tournament:
    tournament = await crud.get_tournament_by_name(session, name)
    if tournament:
        return tournament

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tournament {name} not found"
    )


async def tournaments_all(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Tournament:
    tournaments = await crud_common.read_objs(session, models.Tournament)
    if tournaments:
        return tournaments

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tournaments not found"
    )