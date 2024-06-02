from typing import Annotated, List
from fastapi import Path, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.common_crud import crud as crud_common
from api_v1.courses import crud
from database import models
from database.models.serializer import serializer
from database.helper_for_db import db_helper
from api_v1.courses.schemas import CourseBase


async def course_by_id(
        course_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Course:
    course = await crud_common.read_obj(
        session=session,
        obj_id=course_id,
        obj=models.Course,
    )
    if course:
        return course

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Course {course_id} not found"
    )


async def courses_all(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> List[models.Course]:
    courses = await crud_common.read_objs(session, models.Course)
    if courses:
        return courses

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Courses not found"
    )


async def courses_all_with_holes(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> List[models.Course]:
    courses = await crud.get_courses_with_holes(session)
    if courses:
        return serializer(target=courses)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Courses not found"
    )


async def courses_by_id_with_holes(
        course_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Course:
    course = await crud.get_course_by_id_with_holes(session, course_id)
    if course:
        return serializer(target=course)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Courses not found"
    )

async def course_by_name(
        course_in: Annotated[CourseBase, Body],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Course:
    course = await crud.get_course_by_name(
        session=session,
        name=course_in.name,
    )
    if course:
        return course

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Course {course_in.name} not found"
    )