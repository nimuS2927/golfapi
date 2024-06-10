from typing import Annotated, List, Dict, Any, Optional
from fastapi import Path, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.schemas import UserId
from api_v1.tournaments.schemas import TournamentId
from api_v1.common_crud import crud as crud_common
from api_v1.tournaments import crud
from database import models
from database.helper_for_db import db_helper


async def tournament_by_id_with_course(
        tournament_id: Annotated[int, Path],
        course_status: Annotated[str, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Tournament:
    if course_status == 'False':
        tournament = await crud_common.read_obj(
            session=session,
            obj_id=tournament_id,
            obj=models.Tournament,
        )
    else:
        tournament = await crud.get_tournament_with_course(
            session=session,
            tournament_id=tournament_id,
        )
    if tournament:
        return tournament

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tournament {tournament_id} not found"
    )


async def tournament_by_id(
        tournament_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Tournament:
    tournament = await crud.get_tournament_with_course(
        session=session,
        tournament_id=tournament_id,
    )
    if tournament:
        return tournament

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tournament {tournament_id} not found"
    )


async def tournament_by_id_for_delete(
        tournament_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Optional[Dict[str, Any]]:
    tournament = await crud.get_tournament_for_top(
        session=session,
        tournament_id=tournament_id
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
        detail=f"Tournament '{name}' not found"
    )


async def tournament_for_game(
        user_tg_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> List[models.Tournament]:
    tournaments = await crud.get_tournaments_for_game(session=session, user_tg_id=user_tg_id)
    if tournaments:
        return tournaments

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tournaments not found"
    )


async def tournament_for_top(
        tournament_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Dict[str, Any]:
    tournaments = await crud.get_tournament_for_top(session=session, tournament_id=tournament_id)
    if tournaments:
        return tournaments

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tournament {tournament_id} not found"
    )


async def tournaments_all(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> List[models.Tournament]:
    tournaments = await crud_common.read_objs(session, models.Tournament)
    if tournaments:
        return tournaments

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tournaments not found"
    )


async def nearest_tournament(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> List[models.Tournament]:
    tournaments = await crud.get_nearest_tournament(session)
    if tournaments:
        return tournaments

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tournaments not found"
    )


async def nearest_tournament_without_user(
        tg_user_id: Annotated[UserId, Body],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> List[models.Tournament]:
    tournaments = await crud.get_nearest_tournament_without_user(
        session=session,
        tg_user_id=tg_user_id,
    )
    if tournaments:
        return tournaments

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tournaments not found"
    )


async def tournament_by_id_for_registration(
        tournament_id: Annotated[TournamentId, Body],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Tournament:
    tournament = await crud.get_tournament_with_items_for_registration(
        session=session,
        tournament_id=tournament_id.tournament_id,
    )
    if tournament:
        return tournament

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tournament {tournament_id.tournament_id} not found"
    )


async def tournament_by_id_for_distribute_users(
        tournament_id: Annotated[TournamentId, Body],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Tournament:
    tournament = await crud.get_tournament_with_items_for_distribute_users(
        session=session,
        tournament_id=tournament_id.tournament_id,
    )
    if tournament:
        return tournament

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tournament {tournament_id.tournament_id} not found"
    )
