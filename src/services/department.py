from ..schemas import DepartmentSchema, DepartmentCreateSchema
from ..exceptions import DepartmentNotFoundException, DepartmentConflictException
from ..exceptions import ConflictException
from ..utils.unit_of_work import IUnitOfWork


class DepartmentService:
    @staticmethod
    async def get_departments(uow: IUnitOfWork) -> list[DepartmentSchema]:
        async with uow:
            return await uow.departments.get_all()

    @staticmethod
    async def get_department_by_id(uow: IUnitOfWork, department_id: str) -> DepartmentSchema:
        async with uow:
            department = await uow.departments.get_one(id=department_id)
            if not department:
                raise DepartmentNotFoundException(department_id)
            return department

    @staticmethod
    async def create_department(uow: IUnitOfWork, department: DepartmentCreateSchema) -> str:
        department_dict: dict = department.model_dump()
        async with uow:
            try:
                department: DepartmentSchema = await uow.departments.add_one(data=department_dict)
                await uow.commit()
                return str(department.id)
            except ConflictException:
                raise DepartmentConflictException()

    @staticmethod
    async def edit_department(uow: IUnitOfWork, department_id: str, department: DepartmentSchema) -> DepartmentSchema:
        department_dict: dict = department.model_dump()
        async with uow:
            try:
                is_exists = await uow.departments.is_exists(id=department_id)
                if not is_exists:
                    raise DepartmentNotFoundException(department_id)
                updated_department = await uow.departments.edit_one(updated_data=department_dict, id=department_id)
                await uow.commit()
                return updated_department
            except ConflictException:
                raise DepartmentConflictException()

    @staticmethod
    async def delete_department(uow: IUnitOfWork, department_id: str) -> None:
        async with uow:
            is_exists = await uow.departments.is_exists(id=department_id)
            if not is_exists:
                raise DepartmentNotFoundException(department_id)
            await uow.departments.delete_one(id=department_id)
            await uow.commit()
