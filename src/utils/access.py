from json import JSONDecodeError

from loguru import logger

from fastapi import Request, Depends

from .schema import RoleEnum
from .security import get_current_user
from .unit_of_work import IUnitOfWork, UnitOfWork
from ..exceptions import ForbiddenException
from ..schemas import UserSchema


async def get_request_body(request: Request) -> dict:
    try:
        body = await request.json()
        return body
    except JSONDecodeError:
        return {}


async def check_department_access(user: UserSchema) -> bool:
    ...


async def check_teacher_access(user: UserSchema, body: dict, uow: IUnitOfWork) -> bool:
    department_id_from_user = user.department_id
    department_id_from_teacher = body.get("department_id")

    logger.debug(department_id_from_user)
    logger.debug(department_id_from_teacher)


async def access_control(request: Request,
                         body: dict = Depends(get_request_body),
                         uow: IUnitOfWork = Depends(UnitOfWork)) -> bool:
    from ..services import TeacherService

    is_accessible = False
    user: UserSchema = await get_current_user(request, uow)
    if user.role == RoleEnum.admin:
        return True
    department_id_from_user = user.department_id

    path_parts = request.url.path.split("/")
    resource = path_parts[3]

    match resource:
        case "departments":
            department_id = request.path_params.get("department_id")
            if department_id:
                is_accessible = department_id_from_user == department_id
        case "teachers":
            teacher_id = request.path_params.get("teacher_id")
            department_id_from_body = body.get("department_id")
            if teacher_id:
                teacher = await TeacherService.get_teacher_by_id(uow, teacher_id)
                if department_id_from_body:
                    is_accessible = department_id_from_user == department_id_from_body
                else:
                    is_accessible = department_id_from_user == teacher.department_id
            else:
                if department_id_from_body:
                    is_accessible = department_id_from_user == department_id_from_body
        case _:
            raise ForbiddenException(message="Unknown resource.")

    if not is_accessible:
        raise ForbiddenException(message="You do not have access to this resource")
    return is_accessible


async def check_is_admin(request: Request, uow: IUnitOfWork = Depends(UnitOfWork)) -> bool:
    user: UserSchema = await get_current_user(request, uow)
    if user.role == RoleEnum.admin:
        return user.department_id
    elif user.role == RoleEnum.user:
        raise ForbiddenException(message="User is not an administrator")
    else:
        raise ForbiddenException(message="Unknown role of the user")
