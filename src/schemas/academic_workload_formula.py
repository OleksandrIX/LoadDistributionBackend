from pydantic import BaseModel

from ..utils.schema import IdMixinSchema


class AcademicWorkloadFormulaBase(BaseModel):
    description: str
    workload_name: str
    formula: str


class AcademicWorkloadFormulaCreateSchema(AcademicWorkloadFormulaBase):
    ...


class AcademicWorkloadFormulaUpdateSchema(AcademicWorkloadFormulaBase):
    ...


class AcademicWorkloadFormulaSchema(IdMixinSchema, AcademicWorkloadFormulaBase):
    class Config:
        from_attributes = True
