from uuid import UUID

from pydantic import BaseModel


class EducationComponentsStudyGroupsSchema(BaseModel):
    education_component_id: UUID
    study_group_id: UUID

    class Config:
        from_attributes = True
