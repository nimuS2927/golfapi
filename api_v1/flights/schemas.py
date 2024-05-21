from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Annotated, Optional, List, TYPE_CHECKING
from annotated_types import MinLen, MaxLen

if TYPE_CHECKING:
    from api_v1.tournaments.schemas import Tournament
    from api_v1.users.schemas import User
    from api_v1.scores.schemas import Score
    from api_v1.totalscores.schemas import TotalScore


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
