from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from auth.admins.dependencies import admin_by_id, admin_by_login, admin_by_login_for_superuser, validate_superuser
from database.helper_for_db import db_helper
from auth.admins import crud as auth_crud
from auth.admins.schemas import CreateAdmin, AdminSchemas, SuperUser
from database.models import Admin

router = APIRouter(prefix='/admins', tags=['Admins'])


@router.get('/{admin_id}/', response_model=AdminSchemas)
async def get_admin_by_id(
        admin: AdminSchemas = Depends(admin_by_id),
        superuser: bool = Depends(validate_superuser),
):
    if superuser:
        return admin


@router.get('/', response_model=AdminSchemas)
async def get_admin_by_login(
        login: str,
        password: str,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    admin: Admin = await admin_by_login(
        login=login,
        password=password,
        session=session
    )
    return admin


@router.post(
    '/',
    response_model=AdminSchemas,
    status_code=status.HTTP_201_CREATED
)
async def create_admin(
        admin_in: CreateAdmin,
        superuser: bool = Depends(validate_superuser),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    if superuser:
        return await auth_crud.create_admin(
            session=session,
            admin_in=admin_in,
        )


@router.delete(
    '/{admin_login}/',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_admin(
    superuser: bool = Depends(validate_superuser),
    admin: Admin = Depends(admin_by_login_for_superuser),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    if superuser:
        if admin:
            await session.delete(admin)
            await session.commit()
