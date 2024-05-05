from sqlalchemy import Column, UUID, String, ForeignKey
from sqlalchemy.orm import relationship

from ..utils.database import LoadDistributionBase
from ..utils.model import IdMixin, TimestampMixin


class SpecialtyModel(LoadDistributionBase, IdMixin, TimestampMixin):
    __tablename__ = "specialties"

    specialty_code = Column(String(20), nullable=False)
    specialty_name = Column(String(255), nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False)

    department = relationship("DepartmentModel", back_populates="specialties")
    specializations = relationship("SpecializationModel", back_populates="specialty")
