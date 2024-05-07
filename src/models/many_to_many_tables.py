from sqlalchemy import Table, Column, UUID, ForeignKey

from ..utils.database import LoadDistributionBase

education_components_study_groups = Table(
    "education_components_study_groups",
    LoadDistributionBase.metadata,
    Column("education_component_id", UUID(as_uuid=True), ForeignKey("education_components.id"), primary_key=True),
    Column("study_group_id", UUID(as_uuid=True), ForeignKey("study_groups.id"), primary_key=True)
)
