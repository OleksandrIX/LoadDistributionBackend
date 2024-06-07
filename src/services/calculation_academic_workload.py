from loguru import logger
from functools import reduce

from ..exceptions import DisciplineNotFoundException
from ..schemas import (DisciplineWithRelationships,
                       WorkloadFormulaSchema,
                       AcademicWorkloadCreateSchema,
                       AcademicWorkloadSchema)
from ..utils.calculation_workload import (calculate_hours,
                                          calculation_workload,
                                          convert_to_education_components_per_course)
from ..utils.unit_of_work import IUnitOfWork


class CalculationAcademicWorkloadService:
    @staticmethod
    async def calculation_workload_for_discipline(
            uow: IUnitOfWork,
            discipline_id: str
    ) -> AcademicWorkloadSchema:
        async with uow:
            academic_workload: AcademicWorkloadCreateSchema = AcademicWorkloadCreateSchema(
                discipline_id=discipline_id
            )

            formulas: list[WorkloadFormulaSchema] = await uow.academic_workload_formula.get_all()
            formulas_dict: dict = {formula.workload_name: formula.formula for formula in formulas}

            discipline: DisciplineWithRelationships = await uow.disciplines.get_one(id=discipline_id)
            if not discipline:
                raise DisciplineNotFoundException(discipline_id)

            education_components_per_course = convert_to_education_components_per_course(discipline)

            for course_study, education_component_per_course in education_components_per_course.items():
                study_groups = [
                    study_group
                    for education_component in education_component_per_course
                    for study_group in education_component.study_groups
                ]

                total_listeners = reduce(lambda x, y: x + y, [
                    study_group.number_listeners
                    for study_group in study_groups
                ])

                numbers_of_flows = total_listeners // 80
                lecture_hourse = education_component_per_course[0].semesters[0].academic_hours.lecture_hours
                academic_workload.lecture_hours += calculate_hours(
                    formula=formulas_dict["lecture_hours"],
                    lecture_hours=lecture_hourse,
                    numbers_of_flows=numbers_of_flows,
                )

                for education_component in education_component_per_course:
                    calculation_workload(academic_workload, education_component, formulas_dict)

                academic_workload.consultation_hours = calculate_hours(
                    formula=formulas_dict["consultation_hours"],
                    number_of_groups=len(study_groups),
                    **academic_workload.model_dump()
                )

            saved_academic_workload = await uow.academic_workload.create_one(data=academic_workload.model_dump())
            logger.success(f"Created academic workload for discipline: '{discipline.discipline_name}'")
            await uow.commit()
        return saved_academic_workload
