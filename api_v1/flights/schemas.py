from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Annotated, Optional, List, TYPE_CHECKING
from annotated_types import MinLen, MaxLen

if TYPE_CHECKING:
    from database.models import Tournament, User, Score, TotalScore


class FlightBase(BaseModel):
    tournaments: Optional[List['Tournament']] = None
    users: Optional[List['User']] = None
    scores: Optional[List['Score']] = None
    totalscores: Optional[List['TotalScore']] = None


class CreateFlight(FlightBase):
    pass


class UpdateFlight(FlightBase):
    pass


class UpdateFlightPartial(FlightBase):
    pass


class Flight(FlightBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
