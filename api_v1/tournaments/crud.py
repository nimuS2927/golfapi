from datetime import datetime, timedelta, date
from typing import Optional, List, Dict, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy.orm import selectinload

from api_v1.users.schemas import UserId
from database.models import Tournament, User, TotalScore
from database import models
from database.models.serializer import serializer


async def get_tournament_by_name(
        session: AsyncSession,
        name: str
) -> Optional[Tournament]:
    stmt = select(Tournament).where(Tournament.name == name)
    result: Result = await session.execute(stmt)
    tournament = result.scalar()
    return tournament


async def get_tournament_ge_start_and_le_end(
        session: AsyncSession,
        start: datetime,
        end: Optional[datetime],
) -> Optional[List[Tournament]]:
    if not end:
        stmt = select(Tournament).where(Tournament.start >= start).order_by(Tournament.start)
    else:
        stmt = select(Tournament).where(Tournament.start >= start, Tournament.end <= end).order_by(Tournament.start)
    result: Result = await session.execute(stmt)
    tournaments = result.scalars().all()
    return list(tournaments)


async def get_nearest_tournament_without_user(
        session: AsyncSession,
        tg_user_id: UserId,
) -> Optional[List[Tournament]]:
    id_telegram = tg_user_id.user_tg_id
    today = date.today()
    end = today + timedelta(days=30)
    stmt = (
        select(Tournament)
        # .join(Tournament.users)
        .options(selectinload(Tournament.users))
        .filter(Tournament.start >= today)
        .filter(Tournament.end <= end)
    )
    result: Result = await session.execute(stmt)
    tournaments = result.scalars().all()
    tournaments = list(set(tournaments))
    result_tournaments = []
    for i in tournaments:
        users = i.users
        flag = True
        for user in users:
            if id_telegram == user.id_telegram:
                flag = False
        if flag:
            result_tournaments.append(i)
    return result_tournaments


async def get_nearest_tournament(
        session: AsyncSession,
) -> Optional[List[Tournament]]:
    today = date.today() - timedelta(days=1)
    end = today + timedelta(days=30)
    stmt = select(Tournament).where(Tournament.start >= today, Tournament.end <= end).order_by(Tournament.start)
    result: Result = await session.execute(stmt)
    tournaments = result.scalars().all()
    return list(tournaments)


async def get_tournaments_for_game(
        user_tg_id: int,
        session: AsyncSession,
) -> Optional[List[Tournament]]:
    now = datetime.now()
    stmt = (select(Tournament).
            where(
        # Tournament.status == True,
        Tournament.start <= now,
        Tournament.end >= now
    ).order_by(Tournament.start)
            .options(selectinload(Tournament.users))
            )
    result: Result = await session.execute(stmt)
    tournaments = result.scalars().all()
    result_tournaments = []
    for i_t in tournaments:
        users = i_t.users
        flag = False
        for i_u in users:
            if i_u.id_telegram == user_tg_id:
                flag = True
        if flag:
            result_tournaments.append(i_t)
    return result_tournaments


async def get_tournament_with_items_for_registration(
        session: AsyncSession,
        tournament_id: int,
        users: Optional[List[models.User]] = None,
        flights: Optional[List[models.Flight]] = None,
) -> Optional[Tournament]:
    tournament = await session.get(
        Tournament,
        tournament_id,
        options=(
            selectinload(Tournament.users),
            selectinload(Tournament.flights),
        ),
    )
    if users:
        tournament.users.extend(users)
    if flights:
        tournament.flights.extend(flights)

    return tournament


async def get_tournament_with_items_for_distribute_users(
        session: AsyncSession,
        tournament_id: int,
) -> Optional[Tournament]:
    tournament = await session.get(
        Tournament,
        tournament_id,
        options=(
            selectinload(Tournament.users),
            selectinload(Tournament.flights),
        ),
    )

    return tournament


async def get_tournament_with_course(
        session: AsyncSession,
        tournament_id: int,
) -> Optional[Tournament]:
    tournament = await session.get(
        Tournament,
        tournament_id,
        options=(
            selectinload(Tournament.course),
        ),
    )

    return tournament


async def get_tournament_for_top(
        tournament_id: int,
        session: AsyncSession,
) -> Optional[Dict[str, Any]]:
    stmt = (
        select(Tournament)
        .where(Tournament.id == tournament_id)
        .options(
            selectinload(Tournament.totalscores).options(
                selectinload(TotalScore.user),
                selectinload(TotalScore.scores),
            )
        )
    )
    result: Result = await session.execute(stmt)
    tournament = result.scalar()
    if tournament:
        return serializer(tournament)
    return None
