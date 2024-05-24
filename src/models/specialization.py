from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship

from ..schemas import SpecializationSchema
from ..utils.database import LoadDistributionBase
from ..utils.model import IdMixin, TimestampMixin


class SpecializationModel(LoadDistributionBase, IdMixin, TimestampMixin):
    __tablename__ = "specializations"

    specialization_code = Column(String(20))
    specialization_name = Column(String(255), nullable=False)
    specialty_id = Column(UUID(as_uuid=True), ForeignKey("specialties.id"), nullable=False)

    specialty = relationship("SpecialtyModel", back_populates="specializations")
    education_components = relationship("EducationComponentModel", back_populates="specialization")

    def to_read_model(self) -> SpecializationSchema:
        return SpecializationSchema.from_orm(self)
