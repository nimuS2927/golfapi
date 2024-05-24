from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.helper_for_db import db_helper
from database import models

from api_v1.common_crud import crud as crud_common
from api_v1.flights.dependencies import flight_by_id, flights_all
from api_v1.flights import schemas
from api_v1.flights.schemas import (
    CreateFlight,
    UpdateFlight,
    UpdateFlightPartial,
)


router = APIRouter(prefix='/flight', tags=['Flights'])


@router.get('/', response_model=List[schemas.Flight])
async def get_flights(
        flights: List[models.Flight] = Depends(flights_all),
) -> List[models.Flight]:
    return flights


@router.get('/{flight_id}/', response_model=schemas.Flight)
async def get_flight(
        flight: models.Flight = Depends(flight_by_id),
) -> models.Flight:
    return flight


@router.post(
    '/',
    response_model=schemas.Flight,
    status_code=status.HTTP_201_CREATED
)
async def create_flight(
    flight_in: CreateFlight,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Flight:
    return await crud_common.create_obj(
        session=session,
        obj_in=flight_in,
        obj=models.Flight
    )


@router.put('/{flight_id}/', response_model=schemas.Flight)
async def update_flight(
    flight_update: UpdateFlight,
    flight: models.Flight = Depends(flight_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Flight:
    return await crud_common.update_obj(
        session=session,
        obj=flight,
        obj_update=flight_update,
    )


@router.patch('/{flight_id}/', response_model=schemas.Flight)
async def update_flight_partial(
    flight_update: UpdateFlightPartial,
    flight: models.Flight = Depends(flight_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Flight:
    return await crud_common.update_obj(
        session=session,
        obj=flight,
        obj_update=flight_update,
        partial=True,
    )


@router.delete(
    '/{flight_id}/',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_flight(
        flight: models.Flight = Depends(flight_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud_common.delete_obj(
        session=session,
        obj=flight
    )
