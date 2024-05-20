from pydantic import BaseModel, ConfigDict
from typing import Annotated, Optional
from annotated_types import MinLen, MaxLen


class UserBase(BaseModel):
    id_telegram: int
    first_name: Annotated[str, MinLen(3), MaxLen(50)]
    last_name: Optional[Annotated[str, MinLen(3), MaxLen(50)]]


class CreateUser(UserBase):
    pass


class UpdateUser(UserBase):
    pass


class UpdateUserPartial(UserBase):
    id_telegram: Optional[int] = None
    first_name: Optional[Annotated[str, MinLen(3), MaxLen(50)]] = None
    last_name: Optional[Annotated[str, MinLen(3), MaxLen(50)]] = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
