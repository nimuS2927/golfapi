from pydantic import BaseModel, ConfigDict
from typing import Annotated, Optional, List, TYPE_CHECKING
from annotated_types import MinLen, MaxLen

from api_v1.scores.schemas import Score


class TotalScoreBase(BaseModel):
    id_tournament: int
    total: int
    scores: Optional[List[Score]]
    id_user: Optional[int] = None
    id_flight: Optional[int] = None


class CreateTotalScore(TotalScoreBase):
    pass


class UpdateTotalScore(TotalScoreBase):
    pass


class UpdateTotalScorePartial(TotalScoreBase):
    id_tournament: int = None
    total: int = None


class TotalScore(TotalScoreBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
