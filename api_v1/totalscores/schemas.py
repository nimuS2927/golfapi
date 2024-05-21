from pydantic import BaseModel, ConfigDict
from typing import Annotated, Optional, List, TYPE_CHECKING
from annotated_types import MinLen, MaxLen

if TYPE_CHECKING:
    from api_v1.tournaments.schemas import Tournament
    from api_v1.scores.schemas import Score
    from api_v1.users.schemas import User
    from api_v1.flights.schemas import Flight


class TotalScoreBase(BaseModel):
    id_tournament: int
    total: int
    tournament: Optional['Tournament']
    id_user: Optional[int] = None
    id_flight: Optional[int] = None
    user: Optional['User'] = None
    flight: Optional['Flight'] = None
    scores: Optional[List['Score']] = None


class CreateTotalScore(TotalScoreBase):
    pass


class UpdateTotalScore(TotalScoreBase):
    pass


class UpdateTotalScorePartial(TotalScoreBase):
    id_tournament: int = None
    total: int = None
    tournament: Optional['Tournament'] = None


class TotalScore(TotalScoreBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
