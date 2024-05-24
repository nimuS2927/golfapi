from typing import List, Dict, Any, Union

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from database.helper_for_db import db_helper
from database import models

from api_v1.common_crud import crud as crud_common
from api_v1.flights import crud as crud_flights
from api_v1.tournaments import crud as crud_tournaments
from api_v1.users import dependencies as dep_users
from api_v1.tournaments import dependencies as dep_tournaments

from api_v1.tournaments import schemas as schemas_tournament
from api_v1.flights import schemas as schemas_flights
from database.models.serializer import serializer

router = APIRouter(prefix='/tournaments', tags=['Tournaments'])


@router.get('/name/{tournament_name}/', response_model=schemas_tournament.Tournament)
async def get_tournament_by_name(
        tournament: models.Tournament = Depends(dep_tournaments.tournament_by_name),
) -> models.Tournament:
    return tournament


@router.get('/nearest/', response_model=List[schemas_tournament.Tournament])
async def get_nearest_tournaments(
        tournaments: List[models.Tournament] = Depends(dep_tournaments.nearest_tournament),
) -> List[models.Tournament]:
    return tournaments


@router.get('/{tournament_id}/', response_model=schemas_tournament.Tournament)
async def get_tournament_by_id(
        tournament: models.Tournament = Depends(dep_tournaments.tournament_by_id),
) -> models.Tournament:
    return tournament


@router.get('/', response_model=List[schemas_tournament.Tournament])
async def get_tournaments(
        tournaments: List[models.Tournament] = Depends(dep_tournaments.tournaments_all),
) -> List[models.Tournament]:
    return tournaments


@router.put('/{tournament_id}/', response_model=schemas_tournament.Tournament)
async def update_tournament(
    tournament_update: schemas_tournament.UpdateTournament,
    tournament: models.Tournament = Depends(dep_tournaments.tournament_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Tournament:
    return await crud_common.update_obj(
        session=session,
        obj=tournament,
        obj_update=tournament_update,
    )


@router.patch('/{tournament_id}/', response_model=schemas_tournament.Tournament)
async def update_tournament_partial(
    tournament_update: schemas_tournament.UpdateTournamentPartial,
    tournament: models.Tournament = Depends(dep_tournaments.tournament_by_id),
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
async def delete_tournament(
        tournament: models.Tournament = Depends(dep_tournaments.tournament_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud_common.delete_obj(
        session=session,
        obj=tournament
    )


@router.post('/nearest/', response_model=List[Dict[str, Any]])
async def get_nearest_tournaments(
        tournaments: List[models.Tournament] = Depends(dep_tournaments.nearest_tournament_without_user),
) -> List[models.Tournament]:
    list_dict_tournaments = serializer(target=tournaments)
    return list_dict_tournaments


@router.post(
    '/adduser/',
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, Any],
)
async def add_user_in_tournament(
        tournament: models.Tournament = Depends(dep_tournaments.tournament_by_id_for_registration),
        user: models.User = Depends(dep_users.user_by_tg_id_body),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> dict[str, Any]:
    if user not in tournament.users:
        tournament.users.append(user)
        await session.commit()

    dict_tournament = serializer(target=tournament)
    return dict_tournament


@router.post(
    '/distribute/',
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
)
async def distribute_users_among_flights_in_tournament(
        tournament: models.Tournament = Depends(dep_tournaments.tournament_by_id_for_registration),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> dict[str, Any]:
    users_list: List[models.User] = tournament.users
    flight_with_items = None
    if tournament.status is False:
        for i, user in enumerate(users_list):
            if i % 4 == 0:
                name_flight = f't_{tournament.id}_f_{i // 4 + 1}'
                try:
                    flight_in: schemas_flights.CreateFlight = schemas_flights.CreateFlight(name=name_flight)
                    flight: models.Flight = await crud_flights.create_flight_for_distribute_users(
                        session=session,
                        flight_in=flight_in,
                    )
                    flight_with_items = await crud_flights.get_flight_with_items_by_name(
                        name=name_flight,
                        session=session
                    )
                except:
                    await session.rollback()
                    flight_with_items = await crud_flights.get_flight_with_items_by_name(
                        name=name_flight,
                        session=session
                    )
            if user not in flight_with_items.users:
                flight_with_items.users.append(user)
                await session.commit()
            if tournament not in flight_with_items.tournaments:
                flight_with_items.tournaments.append(tournament)
                await session.commit()
        tournament.status = True
        await session.commit()
    tournament = await crud_tournaments.get_tournament_with_items_for_registration(
        session=session,
        tournament_id=tournament.id,
    )
    dict_tournament = serializer(target=tournament)
    return dict_tournament


@router.post(
    '/',
    response_model=schemas_tournament.Tournament,
    status_code=status.HTTP_201_CREATED
)
async def create_tournament(
    tournament_in: schemas_tournament.CreateTournament,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Tournament:
    tournament: models.Tournament = await crud_common.create_obj(
        session=session,
        obj_in=tournament_in,
        obj=models.Tournament
    )
    # tournament_with_items = await session.get(
    #     models.Tournament,
    #     tournament.id,
    #     options=(selectinload(models.Tournament.flights),)
    # )
    # tournament_dict: Tournament = Tournament.model_validate(tournament)
    # flights_list = []
    # for i in range(tournament.max_flights):
    #     flight = await crud_common.create_obj(
    #         session=session,
    #         obj_in={'tournaments': [tournament_dict]},
    #         obj=models.Flight
    #     )
    #     tournament_with_items.flights.append(flight)
    return tournament



