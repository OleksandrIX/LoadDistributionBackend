from sqlalchemy import select

from ..models import DepartmentModel
from ..schemas import DepartmentWithTeachersSchema, DepartmentWithEducationComponentsSchema
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
        return [row.to_read_model_with_education_components() for row in departments]

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
