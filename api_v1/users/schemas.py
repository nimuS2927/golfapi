from typing import TYPE_CHECKING
from pydantic import BaseModel, ConfigDict
from typing import Annotated, Optional
from annotated_types import MinLen, MaxLen, Ge, Le


class UserBase(BaseModel):
    id_telegram: int
    first_name: Annotated[str, MinLen(3), MaxLen(50)]
    last_name: Optional[Annotated[str, MinLen(3), MaxLen(50)]]
    phone: Annotated[str, MinLen(11), MaxLen(11)]
    handicap: Annotated[float, Ge(-7.), Le(54.)] = 54.
    image_src: str = 'No content yet'
    status: bool = False


class CreateUser(UserBase):
    pass


class UpdateUser(UserBase):
    pass


class UpdateUserPartial(UserBase):
    id_telegram: Optional[int] = None
    first_name: Optional[Annotated[str, MinLen(3), MaxLen(50)]] = None
    last_name: Optional[Annotated[str, MinLen(3), MaxLen(50)]] = None
    handicap: Optional[float] = None
    image_src: Optional[str] = None
    status: Optional[bool] = None
    phone: Optional[Annotated[str, MinLen(3), MaxLen(50)]] = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class UserId(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_tg_id: int
