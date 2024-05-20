from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict


class AdminBase(BaseModel):
    login: Annotated[str, MinLen(3), MaxLen(50)]
    password: str


class CreateAdmin(AdminBase):
    pass


class GetAdmin(AdminBase):
    pass


class AdminSchemas(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    login: Annotated[str, MinLen(3), MaxLen(50)]


class SuperUser(BaseModel):
    login: Annotated[str, MinLen(3), MaxLen(50)]
    password: str
