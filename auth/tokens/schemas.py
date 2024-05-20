from pydantic import BaseModel, ConfigDict
from typing import Optional

from core import c_project


class TokenBase(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class Token(TokenBase):
    model_config = ConfigDict(from_attributes=True)
    refresh_token: Optional[str] = None
    public_key: str = c_project.auth_jwt.public_key_path.read_text()
    algorithm: str = c_project.auth_jwt.algorithm
