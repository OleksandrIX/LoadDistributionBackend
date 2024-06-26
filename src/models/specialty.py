from sqlalchemy import Column, UUID, String, ForeignKey
from sqlalchemy.orm import relationship

from ..schemas import SpecialtySchema
from ..utils.database import LoadDistributionBase
from ..utils.model import IdMixin, TimestampMixin


class SpecialtyModel(LoadDistributionBase, IdMixin, TimestampMixin):
    __tablename__ = "specialties"

    specialty_code = Column(String(20), nullable=False)
    specialty_name = Column(String(255), nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id", ondelete="CASCADE"), nullable=False)

    department = relationship("DepartmentModel", back_populates="specialties")
    specializations = relationship("SpecializationModel", back_populates="specialty")

    def to_read_model(self) -> SpecialtySchema:
        return SpecialtySchema.from_orm(self)
