from sqlalchemy import select

from ..models import EducationComponentModel
from ..schemas import EducationComponenWithWorkloadSchema, ECWithAcademicDataSchema
from ..utils.repository import SQLAlchemyRepository


class EducationComponentRepository(SQLAlchemyRepository):
    model = EducationComponentModel

    async def get_education_component_with_workload(
            self,
            education_component_id: str
    ) -> EducationComponenWithWorkloadSchema:
        query = select(self.model).filter_by(id=education_component_id)
        result = await self.session.execute(query)
        education_component = result.scalars().first()
        return education_component.to_read_model_with_workload()
