from sqlalchemy import Column, UUID, ForeignKey

from ..utils.database import LoadDistributionBase
from ..schemas import EducationComponentsStudyGroupsSchema


class EducationComponentsStudyGroupsModel(LoadDistributionBase):
    __tablename__ = "education_components_study_groups"

    education_component_id = Column(UUID(as_uuid=True), ForeignKey("education_components.id", ondelete="CASCADE"), primary_key=True)
    study_group_id = Column(UUID(as_uuid=True), ForeignKey("study_groups.id", ondelete="CASCADE"), primary_key=True)

    def to_read_model(self) -> EducationComponentsStudyGroupsSchema:
        return EducationComponentsStudyGroupsSchema.from_orm(self)
