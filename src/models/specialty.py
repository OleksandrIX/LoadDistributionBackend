from sqlalchemy import Column, UUID, String, ForeignKey
from sqlalchemy.orm import relationship

from ..schemas import SpecialtySchema
from ..utils.database import LoadDistributionBase
from ..utils.model import IdMixin, TimestampMixin


class SpecialtyModel(LoadDistributionBase, IdMixin, TimestampMixin):
    __tablename__ = "specialties"

    specialty_code = Column(String(20), nullable=False)
    specialty_name = Column(String(255), nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False)

    department = relationship("DepartmentModel", back_populates="specialties")
    specializations = relationship("SpecializationModel", back_populates="specialty")

    def to_read_model(self) -> SpecialtySchema:
        return SpecialtySchema(
            id=self.id,
            specialty_code=self.specialty_code,
            specialty_name=self.specialty_name,
            department_id=str(self.department_id),
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
