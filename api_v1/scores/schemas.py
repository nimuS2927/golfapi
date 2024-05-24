from pydantic import BaseModel, ConfigDict
from typing import Annotated, Optional, List, TYPE_CHECKING
from annotated_types import MinLen, MaxLen


class ScoreBase(BaseModel):
    id_tournament: int
    id_hole: Optional[int]
    id_user: Optional[int]
    id_flight: Optional[int]
    id_total_score: Optional[int]
    impacts: Optional[int]


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
