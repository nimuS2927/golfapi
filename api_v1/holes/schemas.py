from pydantic import BaseModel, ConfigDict
from typing import Annotated, Optional, List, TYPE_CHECKING
from annotated_types import Ge, Le

if TYPE_CHECKING:
    from api_v1.tournaments.schemas import Tournament
    from api_v1.scores.schemas import Score


class HoleBase(BaseModel):
    number: Annotated[int, Ge(1), Le(18)]
    par: Annotated[int, Ge(3), Le(5)]
    difficulty: Annotated[int, Ge(1), Le(18)]


class CreateHole(HoleBase):
    pass


class UpdateHole(HoleBase):
    pass


class UpdateHolePartial(HoleBase):
    number: Optional[Annotated[int, Ge(1), Le(18)]] = None
    par: Optional[Annotated[int, Ge(3), Le(5)]] = None
    difficulty: Optional[Annotated[int, Ge(1), Le(18)]] = None


class Hole(HoleBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
