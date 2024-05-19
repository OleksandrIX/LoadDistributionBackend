from typing import Annotated

from fastapi import Depends

from .security import JWTBearer, get_current_user, check_is_admin
from .unit_of_work import IUnitOfWork, UnitOfWork
from ..schemas import UserSchema

UOWDependencies = Annotated[IUnitOfWork, Depends(UnitOfWork)]
SecurityDependencies = Depends(JWTBearer())
AdminDependencies = Depends(check_is_admin)
CurrentUserDependencies = Annotated[UserSchema, Depends(get_current_user)]
