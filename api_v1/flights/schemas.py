from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Annotated, Optional, List, TYPE_CHECKING
from annotated_types import MinLen, MaxLen

from api_v1.users.schemas import User
from api_v1.tournaments.schemas import Tournament


class FlightBase(BaseModel):
    name: str


class CreateFlight(FlightBase):
    pass


class UpdateFlight(FlightBase):
    users: Optional[List[User]]
    tournaments: Optional[List[Tournament]]


class UpdateFlightPartial(FlightBase):
    users: Optional[List[User]] = None
    tournaments: Optional[List[Tournament]] = None


class Flight(FlightBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
