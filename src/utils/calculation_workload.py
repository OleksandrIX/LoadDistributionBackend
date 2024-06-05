from functools import reduce

from ..schemas import (EducationComponentWithRelationships,
                       DisciplineWithRelationships,
                       AcademicWorkloadCreateSchema)
from ..utils.schema import ReportingTypeEnum


def calculate_hours(formula, **kwargs):
    locals().update(**kwargs)
    exec(formula)
    return locals().get("hours")


def convert_to_education_components_per_course(
        discipline: DisciplineWithRelationships
) -> dict[str, list[EducationComponentWithRelationships]]:
    education_components_per_course: dict[str, list[EducationComponentWithRelationships]] = {}
    for education_component in discipline.education_components:
        if education_component.course_study not in education_components_per_course:
            education_components_per_course[education_component.course_study] = []

        education_components_per_course[education_component.course_study].append(education_component)
    return education_components_per_course


def calculation_workload(
        academic_workload: AcademicWorkloadCreateSchema,
        education_component: EducationComponentWithRelationships,
        formulas_dict: dict,
) -> AcademicWorkloadCreateSchema:
    number_listeners_on_education_component = reduce(lambda x, y: x + y, [
        study_group.number_listeners
        for study_group in education_component.study_groups
    ], 0)

    for semester in education_component.semesters:
        academic_workload.group_hours += calculate_hours(
            formula=formulas_dict["group_hours"],
            group_hours=semester.academic_hours.group_hours,
            number_of_groups=len(education_component.study_groups)
        )

        academic_workload.practical_hours += calculate_hours(
            formula=formulas_dict["practical_hours"],
            practical_hours=semester.academic_hours.practical_hours,
            number_of_groups=len(education_component.study_groups)
        )

        academic_workload.term_papers_conducting_hours += calculate_hours(
            formula=formulas_dict["term_papers_conducting_hours"],
            term_papers=semester.academic_task.term_papers,
            number_listeners=number_listeners_on_education_component,
        )

        academic_workload.control_works_checking_hours += calculate_hours(
            formula=formulas_dict["control_works_checking_hours"],
            modular_control_works=semester.academic_task.modular_control_works,
            calculation_graphic_works=semester.academic_task.calculation_graphic_works,
            number_listeners=number_listeners_on_education_component,
        )

        if semester.reporting_type == ReportingTypeEnum.graded_test:
            academic_workload.graded_tests_conducting_hours += calculate_hours(
                formula=formulas_dict["graded_tests_conducting_hours"],
                number_listeners=number_listeners_on_education_component,
            )
        elif semester.reporting_type == ReportingTypeEnum.exam:
            academic_workload.exams_conducting_hours += calculate_hours(
                formula=formulas_dict["exams_conducting_hours"],
                number_listeners=number_listeners_on_education_component,
                number_of_groups=len(education_component.study_groups)
            )
    return academic_workload
