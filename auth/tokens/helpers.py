from datetime import timedelta
from typing import Optional

from auth.tokens import utils as auth_utils
from core.config import c_project


def create_jwt(
        token_type: str,
        token_data: dict,
        expire_minutes: int = c_project.auth_jwt.access_token_expire_minutes,
        expire_timedelta: Optional[timedelta] = None,
) -> str:
    jwt_payload = {c_project.auth_jwt.token_type_field: token_type}
    jwt_payload.update(token_data)
    return auth_utils.encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta
    )


def create_access_token(sub: str) -> str:
    jwt_payload = {
        'sub': sub
    }
    return create_jwt(
        token_type=c_project.auth_jwt.access_token_type,
        token_data=jwt_payload,
        expire_minutes=c_project.auth_jwt.access_token_expire_minutes,
    )


def create_refresh_token(sub: str) -> str:
    jwt_payload = {
        'sub': sub
    }
    return create_jwt(
        token_type=c_project.auth_jwt.refresh_token_type,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=c_project.auth_jwt.refresh_token_expire_days),
    )

