from ..exceptions import ConflictException
from ..exceptions import DepartmentNotFoundException, DepartmentConflictException
from ..schemas import (DepartmentSchema,
                       DepartmentCreateSchema,
                       DepartmentWithTeachersSchema,
                       DepartmentWithDisciplines,
                       DepartmentWithRelationships)
from ..utils.unit_of_work import IUnitOfWork


class DepartmentService:
    @staticmethod
    async def get_departments(uow: IUnitOfWork) -> list[DepartmentSchema]:
        async with uow:
            return await uow.departments.get_all()

    @staticmethod
    async def get_departments_with_teachers(uow: IUnitOfWork) -> list[DepartmentWithTeachersSchema]:
        async with uow:
            return await uow.departments.get_all_with_teachers()

    @staticmethod
    async def get_departments_with_education_components(
            uow: IUnitOfWork
    ) -> list[DepartmentWithDisciplines]:
        async with uow:
            return await uow.departments.get_all_with_education_components()

    @staticmethod
    async def get_departments_with_relationships(
            uow: IUnitOfWork
    ) -> list[DepartmentWithRelationships]:
        async with uow:
            return await uow.departments.get_all_with_relationships()

    @staticmethod
    async def get_department_by_id(uow: IUnitOfWork, department_id: str) -> DepartmentSchema:
        async with uow:
            department = await uow.departments.get_one(id=department_id)
            if not department:
                raise DepartmentNotFoundException(department_id)
            return department

    @staticmethod
    async def get_deparment_by_id_with_teachers(
            uow: IUnitOfWork,
            department_id: str
    ) -> DepartmentWithTeachersSchema:
        async with uow:
            is_exists = await uow.departments.is_exists(id=department_id)
            if not is_exists:
                raise DepartmentNotFoundException(department_id)
            department = await uow.departments.get_deparment_by_id_with_teachers(department_id)
            return department

    @staticmethod
    async def get_deparment_by_id_with_education_components(
            uow: IUnitOfWork,
            department_id: str
    ) -> DepartmentWithDisciplines:
        async with uow:
            is_exists = await uow.departments.is_exists(id=department_id)
            if not is_exists:
                raise DepartmentNotFoundException(department_id)
            department = await uow.departments.get_department_by_id_with_education_components(department_id)
            return department

    @staticmethod
    async def get_deparment_by_id_with_relationships(
            uow: IUnitOfWork,
            department_id: str
    ) -> DepartmentWithDisciplines:
        async with uow:
            is_exists = await uow.departments.is_exists(id=department_id)
            if not is_exists:
                raise DepartmentNotFoundException(department_id)
            department = await uow.departments.get_department_by_id_with_relationships(department_id)
            return department

    @staticmethod
    async def create_department(uow: IUnitOfWork, department: DepartmentCreateSchema) -> str:
        department_dict: dict = department.model_dump()
        async with uow:
            try:
                department: DepartmentSchema = await uow.departments.create_one(data=department_dict)
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
