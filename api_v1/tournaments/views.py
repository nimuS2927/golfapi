from typing import List, Dict, Any, Union, Optional

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
from api_v1.scores import schemas as schemas_scores
from api_v1.totalscores import schemas as schemas_totalscores
from api_v1.flights import schemas as schemas_flights
from database.models.serializer import serializer

router = APIRouter(prefix='/tournaments', tags=['Tournaments'])


@router.get('/game/{user_tg_id}/', response_model=List[schemas_tournament.Tournament])
async def get_tournament_for_game(
        tournaments: List[models.Tournament] = Depends(dep_tournaments.tournament_for_game),
) -> List[models.Tournament]:
    return tournaments


@router.get('/totalscores/{tournament_id}/', response_model=Dict[str, Any])
async def get_tournament_for_top(
        tournament: Dict[str, Any] = Depends(dep_tournaments.tournament_for_top),
) -> Dict[str, Any]:
    return tournament


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


@router.get('/{tournament_id}/{course_status}/', response_model=Dict[str, Any])
async def get_tournament_by_id(
        tournament: models.Tournament = Depends(dep_tournaments.tournament_by_id_with_course),
) -> Dict[str, Any]:
    result_dict = serializer(target=tournament)
    return result_dict


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
        tournament: Optional[Dict[str, Any]] = Depends(dep_tournaments.tournament_by_id_for_delete),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    if tournament.get('totalscores'):
        for i_ts in tournament.get('totalscores'):
            if i_ts.get('scores'):
                for i_sc in i_ts.get('scores'):
                    score_schema: schemas_scores.Score = schemas_scores.Score.model_validate(i_sc)
                    score = await crud_common.read_obj(
                        session=session,
                        obj_id=score_schema.id,
                        obj=models.Score
                    )
                    await crud_common.delete_obj(
                        session=session,
                        obj=score
                    )
            totalscore_schema: schemas_totalscores.TotalScore = schemas_totalscores.TotalScore.model_validate(i_ts)
            totalscore = await crud_common.read_obj(
                session=session,
                obj_id=totalscore_schema.id,
                obj=models.TotalScore
            )
            await crud_common.delete_obj(
                session=session,
                obj=totalscore
            )
    tournament_model = await crud_common.read_obj(
        session=session,
        obj_id=tournament['id'],
        obj=models.Tournament
    )
    await crud_common.delete_obj(
        session=session,
        obj=tournament_model
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
    response_model=bool,
)
async def distribute_users_among_flights_in_tournament(
        tournament: models.Tournament = Depends(dep_tournaments.tournament_by_id_for_registration),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> bool:
    users_list: List[models.User] = tournament.users
    flights_list: List[models.Flight] = tournament.flights
    users_in_flights = []
    not_full_flights = []
    full_flights_numbers = []
    if flights_list:
        for flight in flights_list:
            flight_with_items = await crud_flights.get_flight_with_items_by_name(
                name=flight.name,
                session=session
            )
            if len(flight_with_items.users) < 4:
                not_full_flights.append(flight_with_items)
            else:
                full_flights_numbers.append(int(flight_with_items.name.split('_')[-1]))
            users_in_flights.extend(flight_with_items.users)
    last_name_flight = None
    if full_flights_numbers:
        full_flights_numbers.sort()
        last_name_flight = f't_{tournament.id}_f_{full_flights_numbers[-1]}'

    users_list = [user for user in users_list if user not in users_in_flights]
    flight_with_items = None
    cur_flight = None
    while users_list:
        cur_user = users_list.pop()
        if not cur_flight:
            if not_full_flights:
                cur_flight = not_full_flights.pop()
                if not last_name_flight:
                    last_name_flight = cur_flight.name
                else:
                    if int(last_name_flight.split('_')[-1]) < int(cur_flight.name.split('_')[-1]):
                        last_name_flight = cur_flight.name
            else:
                if not last_name_flight:
                    last_num = 0
                else:
                    last_num = int(last_name_flight.split('_')[-1])
                name_flight = f't_{tournament.id}_f_{last_num + 1}'
                flight_in: schemas_flights.CreateFlight = schemas_flights.CreateFlight(name=name_flight)
                flight: models.Flight = await crud_flights.create_flight_for_distribute_users(
                    session=session,
                    flight_in=flight_in,
                )
                cur_flight = await crud_flights.get_flight_with_items_by_name(
                    name=name_flight,
                    session=session
                )
        if tournament not in cur_flight.tournaments:
            cur_flight.tournaments.append(tournament)
            await session.commit()
        cur_flight.users.append(cur_user)
        await session.commit()
        if len(cur_flight.users) == 4:
            cur_flight = None
    if not tournament.status:
        tournament.status = True
        await session.commit()
    tournament = await crud_tournaments.get_tournament_with_items_for_registration(
        session=session,
        tournament_id=tournament.id,
    )
    if tournament.status:
        return True
    else:
        return False


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
    return tournament



