from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import c_project

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.admins.dependencies import admin_by_login
from auth.admins.schemas import AdminBase, GetAdmin
from auth.tokens import helpers
from auth.tokens.utils import decode_jwt
from database.helper_for_db import db_helper

from auth.tokens.schemas import Token, TokenBase
from database.models import Admin

router = APIRouter(prefix='/tokens', tags=['Tokens'])


@router.post(
    '/access/',
    response_model=TokenBase,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
)
async def create_access_token(
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    token = credentials.credentials
    if token:
        token_data = decode_jwt(token)
        if token_data['type'] == c_project.auth_jwt.refresh_token_type:
            access_token = helpers.create_access_token(sub=token_data['sub'])
            token = Token(access_token='Bearer ' + access_token)
            return token


@router.post(
    '/full/',
    response_model=Token,
    status_code=status.HTTP_201_CREATED
)
async def create_full_token(
        admin_in: GetAdmin,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    admin: Admin = await admin_by_login(
        admin_in=admin_in,
        session=session
    )
    if admin:
        access_token = helpers.create_access_token(sub=admin.login)
        refresh_token = helpers.create_refresh_token(sub=admin.login)
        token = Token(
            access_token='Bearer ' + access_token,
            refresh_token='Bearer ' + refresh_token,
        )
        return token
