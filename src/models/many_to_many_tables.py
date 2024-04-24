from sqlalchemy import Table, Column, UUID, ForeignKey
from sqlalchemy.orm import relationship

from ..utils.database import Base

education_components_study_groups = Table(
    "education_components_study_groups",
    Base.metadata,
    Column("education_component_id", UUID(as_uuid=True), ForeignKey("education_components.id"), primary_key=True),
    Column("study_group_id", UUID(as_uuid=True), ForeignKey("study_groups.id"), primary_key=True)
)
