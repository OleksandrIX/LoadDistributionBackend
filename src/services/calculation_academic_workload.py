from loguru import logger

from ..schemas import (TeacherSchema,
                       EducationComponentWithAcademicDataSchema,
                       AcademicWorkloadFormulaSchema,
                       AcademicWorkloadCreateSchema)
from ..exceptions import TeacherNotFoundException, EducationComponentNotFoundException
from ..utils.unit_of_work import IUnitOfWork

calculation_workload_formulas = {
    "calculation_lecture_hours": "hours = lecture_hours * number_of_flows",
    "calculation_group_hours": "hours = group_hours * number_of_groups",
    "calculation_practical_hours": "hours = practical_hours * number_of_groups * 2"
}


def calculate_hours(formula, **kwargs):
    locals().update(**kwargs)
    exec(formula)
    return locals().get("hours")


class CalculationAcademicWorkloadService:
    @staticmethod
    async def calculation_classroom_workload(
            uow: IUnitOfWork,
            teacher_id: str,
            disciplines_id: list[str],
    ):
        lecture_hours = 10,
        group_hours = 20,
        practical_hours = 40,
        number_of_flows = 1,
        number_of_groups = 3,
        async with (uow):
            teacher: TeacherSchema = await uow.teachers.get_one(id=teacher_id)
            if not teacher:
                raise TeacherNotFoundException(teacher_id)
            response = {
                "teacher": teacher,
                "academic_workloads": []
            }
            formulas: list[AcademicWorkloadFormulaSchema] = await uow.academic_workload_formula.get_all()
            for discipline_id in disciplines_id:
                education_component: EducationComponentWithAcademicDataSchema = await uow.education_components.get_education_component_by_id_with_academic_data(
                    id=discipline_id)
                if not education_component:
                    raise EducationComponentNotFoundException(discipline_id)

                for semester in education_component.semesters:
                    academic_workload = AcademicWorkloadCreateSchema(
                        teacher_id=teacher_id,
                        education_component_id=discipline_id,
                        semester_number=semester.semester_number
                    )

                    # for formula in formulas:
                    #     setattr(
                    #         academic_workload,
                    #         formula.workload_name,
                    #         calculate_hours(
                    #             formula.formula,
                    #             education_component
                    #             lecture_hours=semester.academic_hours.lecture_hours,
                    #             group_hours=semester.academic_hours.group_hours,
                    #             practical_hours=semester.academic_hours.practical_hours,
                    #         )
                    #     )
                    logger.debug(academic_workload)
                    response.get("academic_workloads").append(academic_workload)
            # saved_academic_workload = await uow.academic_workload.create_one(data=academic_workload.model_dump())
            # return saved_academic_workload
            return response
