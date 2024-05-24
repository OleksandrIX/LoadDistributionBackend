from json import JSONDecodeError

from fastapi import Request, Depends

from .schema import RoleEnum
from .security import get_current_user
from .unit_of_work import IUnitOfWork, UnitOfWork
from ..exceptions import ForbiddenException
from ..schemas import UserSchema


def has_access(user_department_id: str, department_id: str) -> bool:
    return user_department_id == department_id


async def get_request_body(request: Request) -> dict:
    try:
        body = await request.json()
        return body
    except JSONDecodeError:
        return {}


async def check_access_to_teachers(request: Request, body: dict, user_department_id: str, uow: IUnitOfWork) -> bool:
    from ..services import TeacherService

    teacher_id = request.path_params.get("teacher_id")
    department_id = body.get("department_id")

    if teacher_id:
        if department_id:
            return has_access(user_department_id, department_id)
        else:
            teacher = await TeacherService.get_teacher_by_id(uow, teacher_id)
            return has_access(user_department_id, teacher.department_id)
    else:
        return has_access(user_department_id, department_id) if department_id else False


async def access_control(
        request: Request,
        body: dict = Depends(get_request_body),
        uow: IUnitOfWork = Depends(UnitOfWork)
) -> bool:
    user: UserSchema = await get_current_user(request, uow)
    if user.role == RoleEnum.admin:
        return True

    user_department_id = user.department_id
    path_parts = request.url.path.split("/")
    resource = path_parts[3]

    match resource:
        case "departments":
            department_id = request.path_params.get("department_id")
            is_accessible = has_access(user_department_id, department_id) if department_id else False
        case "teachers":
            is_accessible = await check_access_to_teachers(request, body, user_department_id, uow)
        case _:
            raise ForbiddenException(message="Unknown resource.")

    if not is_accessible:
        raise ForbiddenException(message="You do not have access to this resource.")
    return is_accessible


async def check_is_admin(request: Request, uow: IUnitOfWork = Depends(UnitOfWork)) -> bool:
    user: UserSchema = await get_current_user(request, uow)
    if user.role == RoleEnum.admin:
        return user.department_id
    elif user.role == RoleEnum.user:
        raise ForbiddenException(message="User is not an administrator")
    else:
        raise ForbiddenException(message="Unknown role of the user")
