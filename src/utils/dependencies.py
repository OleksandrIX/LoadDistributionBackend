from typing import Annotated

from fastapi import Depends

from .access import check_is_admin, access_control
from .security import JWTBearer, get_current_user
from .unit_of_work import IUnitOfWork, UnitOfWork
from ..schemas import UserSchema

UOWDependencies = Annotated[IUnitOfWork, Depends(UnitOfWork)]
CurrentUserDependencies = Annotated[UserSchema, Depends(get_current_user)]
SecurityDependencies = Depends(JWTBearer())
AdminDependencies = Depends(check_is_admin)
AccessControlDependencies = Depends(access_control)
