from pydantic import BaseModel, ConfigDict
from typing import Annotated, Optional, List, TYPE_CHECKING
from annotated_types import MinLen, MaxLen

if TYPE_CHECKING:
    from api_v1.tournaments.schemas import Tournament
    from api_v1.holes.schemas import Hole
    from api_v1.users.schemas import User
    from api_v1.flights.schemas import Flight
    from api_v1.totalscores.schemas import TotalScore


class ScoreBase(BaseModel):
    id_tournament: int
    id_hole: Optional[int]
    id_user: Optional[int]
    id_flight: Optional[int]
    id_total_score: Optional[int]
    impacts: Optional[int]
    tournaments: Optional[List['Tournament']] = None
    hole: Optional[List['Hole']] = None
    user: Optional[List['User']] = None
    flight: Optional[List['Flight']] = None
    totalscore: Optional[List['TotalScore']] = None


class CreateScore(ScoreBase):
    pass


class UpdateScore(ScoreBase):
    pass


class UpdateScorePartial(ScoreBase):
    id_tournament: int = None
    id_hole: Optional[int] = None
    id_user: Optional[int] = None
    id_flight: Optional[int] = None
    id_total_score: Optional[int] = None
    impacts: Optional[int] = None


class Score(ScoreBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
