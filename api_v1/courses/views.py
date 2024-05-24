from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.helper_for_db import db_helper
from database import models

from api_v1.common_crud import crud as crud_common
from api_v1.courses.dependencies import course_by_id, course_by_name, courses_all
from api_v1.courses import schemas
from api_v1.courses.schemas import (
    CreateCourse,
    UpdateCourse,
    UpdateCoursePartial,
)


router = APIRouter(prefix='/course', tags=['Courses'])


@router.get('/', response_model=List[schemas.Course])
async def get_courses(
        courses: List[models.Course] = Depends(courses_all),
) -> List[models.Course]:
    return courses


@router.get('/{course_id}/', response_model=schemas.Course)
async def get_course_by_id(
        course: models.Course = Depends(course_by_id),
) -> models.Course:
    return course


@router.post('/name/', response_model=schemas.Course)
async def get_course_by_number(
        course: models.Course = Depends(course_by_name),
) -> models.Course:
    return course


@router.post(
    '/',
    response_model=schemas.Course,
    status_code=status.HTTP_201_CREATED
)
async def create_course(
    course_in: CreateCourse,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Course:
    return await crud_common.create_obj(
        session=session,
        obj_in=course_in,
        obj=models.Course
    )


@router.put('/{course_id}/', response_model=schemas.Course)
async def update_course(
    course_update: UpdateCourse,
    course: models.Course = Depends(course_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Course:
    return await crud_common.update_obj(
        session=session,
        obj=course,
        obj_update=course_update,
    )


@router.patch('/{course_id}/', response_model=schemas.Course)
async def update_course_partial(
    course_update: UpdateCoursePartial,
    course: models.Course = Depends(course_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Course:
    return await crud_common.update_obj(
        session=session,
        obj=course,
        obj_update=course_update,
        partial=True,
    )


@router.delete(
    '/{course_id}/',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_course(
        course: models.Course = Depends(course_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud_common.delete_obj(
        session=session,
        obj=course
    )
