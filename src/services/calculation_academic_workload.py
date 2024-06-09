from loguru import logger

from ..exceptions import DisciplineNotFoundException, EducationComponentNotFoundException
from ..schemas import (AcademicWorkloadCreateSchema,
                       AcademicWorkloadSchema)
from ..utils.calculation_workload import (calculate_hours,
                                          calculation_workload,
                                          convert_to_education_components_per_course)
from ..utils.unit_of_work import IUnitOfWork


class CalculationAcademicWorkloadService:
    @staticmethod
    async def save_academic_workload(
            uow: IUnitOfWork,
            academic_workload: AcademicWorkloadCreateSchema
    ) -> AcademicWorkloadSchema:
        async with uow:
            saved_academic_workload = await uow.academic_workload.create_one(data=academic_workload.model_dump())
            await uow.commit()
            return saved_academic_workload

    @staticmethod
    async def _calculate_workload(
            uow: IUnitOfWork,
            discipline_id: str = None,
            education_component_id: str = None,
            education_component_ids: list[str] = None,
            study_group_id: str = None,
            lecture_only: bool = False,
            without_lecture: bool = False,
    ) -> AcademicWorkloadSchema:
        async with uow:
            academic_workload = AcademicWorkloadCreateSchema()
            formulas = await uow.academic_workload_formula.get_all()
            formulas_dict = {formula.workload_name: formula.formula for formula in formulas}

            if discipline_id:
                discipline = await uow.disciplines.get_one(id=discipline_id)
                if not discipline:
                    raise DisciplineNotFoundException(discipline_id)
                education_components = discipline.education_components
            elif education_component_id:
                education_component = await uow.education_components.get_one(id=education_component_id)
                if not education_component:
                    raise EducationComponentNotFoundException(education_component_id)
                education_components = [education_component]
            else:
                education_components = []
                for ec_id in education_component_ids:
                    ec = await uow.education_components.get_one(id=ec_id)
                    education_components.append(ec)

            education_components_per_course = convert_to_education_components_per_course(education_components)

            for course_study, education_component_per_course in education_components_per_course.items():
                if not study_group_id:
                    study_groups = [
                        study_group
                        for education_component in education_component_per_course
                        for study_group in education_component.study_groups
                    ]
                else:
                    study_groups = [await uow.study_groups.get_one(id=study_group_id)]

                number_of_groups = len(study_groups)
                number_listeners = sum(study_group.number_listeners for study_group in study_groups)
                numbers_of_flows = -(-number_listeners // 100)
                lecture_hours = education_component_per_course[0].semesters[0].academic_hours.lecture_hours

                if not without_lecture:
                    academic_workload.lecture_hours += calculate_hours(
                        formula=formulas_dict["lecture_hours"],
                        lecture_hours=lecture_hours,
                        numbers_of_flows=numbers_of_flows,
                    )

                if not lecture_only:
                    for education_component in education_component_per_course:
                        academic_workload = calculation_workload(
                            academic_workload,
                            education_component,
                            formulas_dict,
                            number_listeners,
                            number_of_groups
                        )

                academic_workload.consultation_hours = calculate_hours(
                    formula=formulas_dict["consultation_hours"],
                    number_of_groups=len(study_groups),
                    **academic_workload.model_dump()
                )

            return academic_workload

    @staticmethod
    async def calculation_workload_for_discipline(uow: IUnitOfWork, discipline_id: str) -> AcademicWorkloadSchema:
        return await CalculationAcademicWorkloadService._calculate_workload(
            uow,
            discipline_id=discipline_id
        )

    @staticmethod
    async def calculation_workload_for_education_component(
            uow: IUnitOfWork,
            education_component_id: str
    ) -> AcademicWorkloadCreateSchema:
        return await CalculationAcademicWorkloadService._calculate_workload(
            uow,
            education_component_id=education_component_id
        )

    @staticmethod
    async def calculation_group_workload(
            uow: IUnitOfWork,
            education_component_id: str,
            study_group_id: str,
    ) -> AcademicWorkloadCreateSchema:
        return await CalculationAcademicWorkloadService._calculate_workload(
            uow,
            education_component_id=education_component_id,
            study_group_id=study_group_id,
            without_lecture=True,
        )

    @staticmethod
    async def calculation_without_lecture_workload(
            uow: IUnitOfWork,
            education_component_id: str
    ) -> AcademicWorkloadCreateSchema:
        return await CalculationAcademicWorkloadService._calculate_workload(
            uow,
            education_component_id=education_component_id,
            without_lecture=True
        )

    @staticmethod
    async def calculation_academic_workload_for_education_components(
            uow: IUnitOfWork,
            education_component_ids: list[str]
    ) -> AcademicWorkloadCreateSchema:
        return await CalculationAcademicWorkloadService._calculate_workload(
            uow,
            education_component_ids=education_component_ids
        )

    @staticmethod
    async def calculation_lecture_workload(
            uow: IUnitOfWork,
            education_component_ids: list[str]
    ) -> AcademicWorkloadCreateSchema:
        return await CalculationAcademicWorkloadService._calculate_workload(
            uow,
            education_component_ids=education_component_ids,
            lecture_only=True
        )
