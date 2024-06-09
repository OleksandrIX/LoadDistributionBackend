from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship

from ..schemas import SpecializationSchema
from ..utils.database import LoadDistributionBase
from ..utils.model import IdMixin, TimestampMixin


class SpecializationModel(LoadDistributionBase, IdMixin, TimestampMixin):
    __tablename__ = "specializations"

    specialization_code = Column(String(20))
    specialization_name = Column(String(255), nullable=False)
    specialty_id = Column(UUID(as_uuid=True), ForeignKey("specialties.id", ondelete="CASCADE"), nullable=False)

    specialty = relationship(
        argument="SpecialtyModel",
        back_populates="specializations",
        lazy="selectin"
    )

    education_components = relationship(
        argument="EducationComponentModel",
        back_populates="specialization",
        lazy="selectin"
    )

    def to_read_model(self) -> SpecializationSchema:
        return SpecializationSchema.from_orm(self)
