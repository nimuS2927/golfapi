from typing import Optional, Union, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from api_v1.users.schemas import CreateUser, UpdateUser, UpdateUserPartial
from api_v1.tournaments.schemas import CreateTournament, UpdateTournament, UpdateTournamentPartial
from api_v1.totalscores.schemas import CreateTotalScore, UpdateTotalScore, UpdateTotalScorePartial
from api_v1.scores.schemas import CreateScore, UpdateScore, UpdateScorePartial
from api_v1.flights.schemas import CreateFlight, UpdateFlight, UpdateFlightPartial
from api_v1.holes.schemas import CreateHole, UpdateHole, UpdateHolePartial
from auth.admins.schemas import CreateAdmin
from database.models import User, Admin, Tournament, Score, TotalScore, Flight, Hole


OBJECTS = [User, Admin, Tournament, Score, TotalScore, Flight, Hole]
OBJ_CREATE = [
    CreateUser,
    CreateScore,
    CreateTotalScore,
    CreateTournament,
    CreateHole,
    CreateFlight,
]
OBJ_UPDATE = [
    UpdateUser,
    UpdateUserPartial,
    UpdateScore,
    UpdateScorePartial,
    UpdateTotalScore,
    UpdateTotalScorePartial,
    UpdateTournament,
    UpdateTournamentPartial,
    UpdateHole,
    UpdateHolePartial,
    UpdateFlight,
    UpdateFlightPartial,
]


async def create_obj(
    session: AsyncSession,
    obj_in: Union[*OBJ_CREATE],
    obj: Union[*OBJECTS]
) -> Union[*OBJECTS]:
    obj_ = obj(**obj_in.model_dump())
    session.add(obj_)
    await session.commit()
    return obj_


async def read_obj(
    session: AsyncSession,
    obj_id: int,
    obj: Union[*OBJECTS]
) -> Optional[Union[*OBJECTS]]:
    return await session.get(obj, obj_id)


async def read_objs(
    session: AsyncSession,
    obj: Union[*OBJECTS]
) -> Optional[List[Union[*OBJECTS]]]:
    stmt = select(obj).order_by(obj.id)
    result: Result = await session.execute(stmt)
    objs = result.scalars().all()
    return list(objs)


async def update_obj(
    session: AsyncSession,
    obj: Union[*OBJECTS],
    obj_update: Union[*OBJ_UPDATE],
    partial: bool = False,
) -> Union[*OBJECTS]:
    for name, value in obj_update.model_dump(exclude_unset=partial).items():
        setattr(obj, name, value)
    await session.commit()
    return obj


async def delete_obj(
    session: AsyncSession,
    obj: Union[*OBJECTS],
) -> None:
    await session.delete(obj)
    await session.commit()
