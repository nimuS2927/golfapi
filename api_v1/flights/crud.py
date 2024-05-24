from datetime import datetime, timedelta, date
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy.orm import selectinload

from database import models
from . import schemas


# async def get_flight_with_items_for_distribute_users(
#     session: AsyncSession,
#     flight_id: int,
# ) -> Optional[models.Flight]:
#     flight = await session.get(
#         models.Flight,
#         flight_id,
#         options=(
#             selectinload(models.Flight.users),
#             selectinload(models.Flight.tournaments),
#         ),
#     )
#
#     return flight


async def create_flight_for_distribute_users(
        session: AsyncSession,
        flight_in: schemas.CreateFlight,
) -> models.Flight:
    flight = models.Flight(**flight_in.model_dump())
    session.add(flight)
    await session.commit()
    return flight


async def get_flight_with_items_by_name(
        session: AsyncSession,
        name: str,
) -> models.Flight:
    try:
        stmt = select(
            models.Flight).options(
            selectinload(models.Flight.users),
            selectinload(models.Flight.tournaments)
        ).where(models.Flight.name == name)
    except Exception as ex:
        print(ex)
        stmt = None
    try:
        result: Result = await session.execute(stmt)
    except Exception as ex:
        print(ex)
        result = None
    try:
        flight = result.scalar()
    except Exception as ex:
        print(ex)
        flight = None
    return flight
