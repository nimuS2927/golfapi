from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Annotated, Optional, List, TYPE_CHECKING
from annotated_types import MinLen, MaxLen

if TYPE_CHECKING:
    from database.models import Flight, Hole, User, Score


class TournamentBase(BaseModel):
    name: Annotated[str, MinLen(3), MaxLen(300)]
    max_flights: int
    start: datetime
    end: Optional[datetime] = None
    hcp: Optional[int] = None
    flights: Optional[List['Flight']] = None
    holes: Optional[List['Hole']] = None
    users: Optional[List['User']] = None
    scores: Optional[List['Score']] = None


class CreateTournament(TournamentBase):
    pass


class UpdateTournament(TournamentBase):
    pass


class UpdateTournamentPartial(TournamentBase):
    name: Optional[Annotated[str, MinLen(3), MaxLen(300)]] = None
    max_flights: Optional[int] = None
    start: Optional[datetime] = None


class Tournament(TournamentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
