from pydantic import BaseModel, Field

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
    military_rank: MilitaryRankEnum
    academic_rank: AcademicRankEnum
    scientific_degree: ScientificDegreeEnum
    years_of_service: int = Field(..., ge=1, le=50)
    department_id: str


class TeacherCreateSchema(TeacherBase):
    ...


class TeacherUpdateSchema(TeacherBase):
    ...


class TeacherSchema(TimestampMixinSchema, IdMixinSchema, TeacherBase):
    ...
