from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
import jwt

from core.config import c_project


def encode_jwt(
    payload: dict,
    private_key: str = c_project.auth_jwt.private_key_path.read_text(),
    algorithm: str = c_project.auth_jwt.algorithm,
    expire_minutes: int = c_project.auth_jwt.access_token_expire_minutes,
    expire_timedelta: Optional[timedelta] = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = c_project.auth_jwt.public_key_path.read_text(),
    algorithm: str = c_project.auth_jwt.algorithm,
) -> dict:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Basic"},
    )
    try:
        decoded = jwt.decode(
            token,
            public_key,
            algorithms=[algorithm],
        )
        return decoded
    except jwt.ExpiredSignatureError:
        unauthed_exc.detail = "Expired token"
        raise unauthed_exc
    except jwt.InvalidTokenError:
        unauthed_exc.detail = "Invalid token"
        raise unauthed_exc
