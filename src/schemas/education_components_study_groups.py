from pydantic import BaseModel


class EducationComponentsStudyGroupsSchema(BaseModel):
    education_component_id: str
    study_group_id: str
