from typing import Optional
from pydantic import BaseModel, Field, field_validator

from ..utils.schema import (IdMixinSchema,
                            TimestampMixinSchema,
                            PositionEnum,
                            MilitaryRankEnum,
                            AcademicRankEnum,
                            ScientificDegreeEnum)


class TeacherBase(BaseModel):
    first_name: str = Field(..., max_length=30)
    last_name: str = Field(..., max_length=30)
    middle_name: str = Field(..., max_length=30)
    position: PositionEnum
    military_rank: Optional[MilitaryRankEnum] = None
    academic_rank: Optional[AcademicRankEnum] = None
    scientific_degree: Optional[ScientificDegreeEnum] = None
    years_of_service: Optional[int] = Field(None, ge=1, le=50)
    teacher_rate: float = Field(..., ge=0.25, le=5.00)
    is_civilian: bool
    department_id: str

    @classmethod
    @field_validator("military_rank", "years_of_service", mode="before")
    def check_military_fields(cls, v, info):
        is_civilian = info.data.get("is_civilian")
        if is_civilian is not None:
            if is_civilian:
                if info.field_name == "military_rank" and v is not None:
                    raise ValueError("military_rank must be None if is_civilian is True")
                if info.field_name == "years_of_service" and v is not None:
                    raise ValueError("years_of_service must be None if is_civilian is True")
            else:
                if info.field_name == "military_rank" and v is None:
                    raise ValueError("military_rank cannot be None if is_civilian is False")
                if info.field_name == "years_of_service" and v is None:
                    raise ValueError("years_of_service cannot be None if is_civilian is False")
        return v


class TeacherCreateSchema(TeacherBase):
    ...


class TeacherUpdateSchema(TeacherBase):
    ...


class TeacherSchema(TimestampMixinSchema, IdMixinSchema, TeacherBase):
    ...
