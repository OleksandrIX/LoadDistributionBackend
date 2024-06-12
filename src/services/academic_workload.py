from ..exceptions import ConflictException
from ..schemas import (AcademicWorkloadTeacherCreateSchema,
                       AcademicWorkloadTeacherSchema,
                       AcademicWorkloadSchema)
from ..utils.unit_of_work import IUnitOfWork


class AcademicWorkloadService:
    @staticmethod
    async def save_workload_for_teacher(
            uow: IUnitOfWork,
            discipline_id: str,
            teacher_id: str,
            semester_number: int,
            academic_workload: AcademicWorkloadSchema
    ):
        academic_workload_teacher = AcademicWorkloadTeacherCreateSchema(
            semester_number=semester_number,
            academic_workload_id=academic_workload.id,
            discipline_id=discipline_id,
            teacher_id=teacher_id
        ).model_dump()
        async with uow:
            try:
                department: AcademicWorkloadTeacherSchema = await uow.academic_workload_teacher.create_one(
                    data=academic_workload_teacher)
                await uow.commit()
                return str(department.id)
            except ConflictException:
                raise ConflictException(message="Academic workload with this teacher already exists")
