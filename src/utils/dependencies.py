from typing import Annotated
from fastapi import Depends

from .unit_of_work import IUnitOfWork, UnitOfWork
from .security import JWTBearer

UOWDependencies = Annotated[IUnitOfWork, Depends(UnitOfWork)]
SecurityDependencies = Depends(JWTBearer())
