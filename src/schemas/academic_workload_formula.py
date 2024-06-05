from pydantic import BaseModel

from ..utils.schema import IdMixinSchema


class WorkloadFormulaBase(BaseModel):
    description: str
    workload_name: str
    formula: str


class WorkloadFormulaCreateSchema(WorkloadFormulaBase):
    ...


class WorkloadFormulaUpdateSchema(WorkloadFormulaBase):
    ...


class WorkloadFormulaSchema(IdMixinSchema, WorkloadFormulaBase):
    class Config:
        from_attributes = True
