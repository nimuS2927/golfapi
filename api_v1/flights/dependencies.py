from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.common_crud import crud as crud_common
from database import models
from database.helper_for_db import db_helper


async def flight_by_id(
        flight_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Flight:
    flight = await crud_common.read_obj(
        session=session,
        obj_id=flight_id,
        obj=models.Flight,
    )
    if flight:
        return flight

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Flight {flight_id} not found"
    )


async def flights_all(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Flight:
    flights = await crud_common.read_objs(session, models.Flight)
    if flights:
        return flights

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Flights not found"
    )
