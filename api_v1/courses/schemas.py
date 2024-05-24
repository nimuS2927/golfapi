from pydantic import BaseModel, ConfigDict
from typing import Annotated, Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from api_v1.tournaments.schemas import Tournament
    from api_v1.holes.schemas import Hole


class CourseBase(BaseModel):
    name: str


class CreateCourse(CourseBase):
    pass


class UpdateCourse(CourseBase):
    pass


class UpdateCoursePartial(CourseBase):
    name: str = None


class Course(CourseBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
