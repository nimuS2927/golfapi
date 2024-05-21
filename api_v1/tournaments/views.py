from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.helper_for_db import db_helper
from database import models

from api_v1.common_crud import crud as crud_common
from api_v1.tournaments.dependencies import tournament_by_id, tournament_by_name, tournaments_all
from api_v1.tournaments import schemas
from api_v1.tournaments.schemas import (
    CreateTournament,
    UpdateTournament,
    UpdateTournamentPartial,
)


router = APIRouter(prefix='/tournament', tags=['Tournaments'])


@router.get('/', response_model=List[schemas.Tournament])
async def get_tournaments(
        tournaments: List[models.Tournament] = Depends(tournaments_all),
) -> List[models.Tournament]:
    return tournaments


@router.get('/{tournament_id}/', response_model=schemas.Tournament)
async def get_tournament(
        tournament: models.Tournament = Depends(tournament_by_id),
) -> models.Tournament:
    return tournament


@router.get('/{tournament_name}/', response_model=schemas.Tournament)
async def get_tournament(
        tournament: models.Tournament = Depends(tournament_by_name),
) -> models.Tournament:
    return tournament


@router.post(
    '/',
    response_model=schemas.Tournament,
    status_code=status.HTTP_201_CREATED
)
async def create_tournament(
    tournament_in: CreateTournament,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Tournament:
    return await crud_common.create_obj(
        session=session,
        obj_in=tournament_in,
        obj=models.Tournament
    )


@router.put('/{tournament_id}/', response_model=schemas.Tournament)
async def update_tournament(
    tournament_update: UpdateTournament,
    tournament: models.Tournament = Depends(tournament_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Tournament:
    return await crud_common.update_obj(
        session=session,
        obj=tournament,
        obj_update=tournament_update,
    )


@router.patch('/{tournament_id}/', response_model=schemas.Tournament)
async def update_tournament_partial(
    tournament_update: UpdateTournamentPartial,
    tournament: models.Tournament = Depends(tournament_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Tournament:
    return await crud_common.update_obj(
        session=session,
        obj=tournament,
        obj_update=tournament_update,
        partial=True,
    )


@router.delete(
    '/{tournament_id}/',
    status_code=status.HTTP_204_NO_CONTENT
)
async def update_tournament(
        tournament: models.Tournament = Depends(tournament_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud_common.delete_obj(
        session=session,
        obj=tournament
    )
