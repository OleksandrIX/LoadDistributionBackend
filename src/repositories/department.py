from sqlalchemy import select
from loguru import logger

from ..models import DepartmentModel
from ..schemas import DepartmentWithTeachersSchema, DepartmentWithEducationComponentsSchema, DepartmentWithRelationships
from ..utils.repository import SQLAlchemyRepository


class DepartmentRepository(SQLAlchemyRepository):
    model = DepartmentModel

    async def get_all_with_teachers(self, **filter_by) -> list[DepartmentWithTeachersSchema]:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        departments = result.scalars().all()
        return [row.to_read_model_with_teachers() for row in departments]

    async def get_all_with_education_components(self, **filter_by) -> list[DepartmentWithEducationComponentsSchema]:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        departments = result.scalars().all()
        departments = [row.to_read_model_with_education_components() for row in departments]
        return departments

    async def get_all_with_relationships(self, **filter_by) -> list[DepartmentWithRelationships]:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        departments = result.scalars().all()
        departments = [row.to_read_model_with_relationships() for row in departments]
        return departments

    async def get_deparment_by_id_with_teachers(self, department_id: str) -> DepartmentWithTeachersSchema:
        query = select(self.model).filter_by(id=department_id)
        result = await self.session.execute(query)
        department = result.scalars().first().to_read_model_with_teachers()
        return department

    async def get_department_by_id_with_education_components(
            self,
            department_id: str
    ) -> DepartmentWithEducationComponentsSchema:
        query = select(self.model).filter_by(id=department_id)
        result = await self.session.execute(query)
        department = result.scalars().first().to_read_model_with_education_components()
        return department

    async def get_department_by_id_with_relationships(self, department_id: str) -> DepartmentWithRelationships:
        query = select(self.model).filter_by(id=department_id)
        result = await self.session.execute(query)
        department = result.scalars().first().to_read_model_with_relationships()
        return department
