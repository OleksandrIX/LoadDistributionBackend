from typing import Annotated
from fastapi import Depends

from .unit_of_work import IUnitOfWork, UnitOfWork

UOWDependencies = Annotated[IUnitOfWork, Depends(UnitOfWork)]
