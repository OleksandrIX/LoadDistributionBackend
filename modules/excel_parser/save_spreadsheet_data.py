import uuid
from loguru import logger

from .spreadsheet_schemas import *

from src.utils.database import session_factory
from src.models import *


def get_current_semester_from_course_and_semester_number(course: int, semester: int) -> int:
    """Function to get the current semester from course number and semester number"""
    return semester + (course - 1) * 2


def get_spreadsheet_data(spreadsheet_block: dict) -> SpreadsheetBlockSchema:
    """Function to get the spreadsheet data from the spreadsheet block"""
    try:
        spreadsheet_block_data = SpreadsheetBlockSchema(
            specialty_code=int(str(spreadsheet_block["specialty"]).split()[0].strip()),
            specialization_name=str(spreadsheet_block["specialization"]).strip(),
            course_study=int(spreadsheet_block["course_study"]),
            education_degree=str(spreadsheet_block["education_degree"]).strip())

        for group in str(spreadsheet_block["study_groups"]).split(","):
            splited_group: list[str] = group.strip().split()
            group_number: str = str(splited_group[0].strip())
            number_listeners: int = int(splited_group[-1].strip().replace("(", "").replace(")", ""))
            spreadsheet_block_data.study_groups.append((group_number, number_listeners))

        return spreadsheet_block_data
    except Exception as err:
        logger.error(err)


def create_semester_model_from_schema(semester_schema: SemesterSchema, course_study: int) -> SemesterModel:
    """Function to create a semester, academic hours and academic task model from a semester schema"""
    semester: SemesterModel = SemesterModel(
        semester_number=get_current_semester_from_course_and_semester_number(
            course=course_study,
            semester=semester_schema.semester_number
        ),
        total_amount_hours=semester_schema.total_amount_hours
    )

    reporting_type = semester_schema.reporting_type
    if reporting_type:
        semester.reporting_type = reporting_type.name
    else:
        semester.reporting_type = None

    academic_hours_schema = semester_schema.academic_hours
    semester.academic_hours = AcademicHoursModel(
        amount_classroom_hours=academic_hours_schema.amount_classroom_hours,
        lecture_hours=academic_hours_schema.lecture_hours,
        group_hours=academic_hours_schema.group_hours,
        practical_hours=academic_hours_schema.practical_hours,
        self_study_hours=academic_hours_schema.self_study_hours,
        semester=semester
    )

    academic_task_schema = semester_schema.academic_task
    semester.academic_task = AcademicTaskModel(
        term_papers=academic_task_schema.term_papers,
        modular_control_works=academic_task_schema.modular_control_works,
        essays=academic_task_schema.essays,
        calculation_graphic_works=academic_task_schema.calculation_graphic_works,
    )

    return semester


def processing_spreadsheet_data(spreadsheet_blocks: list[dict]) -> None:
    """Function to process spreadsheet and save it to database"""
    for spreadsheet_block in spreadsheet_blocks:
        spreadsheet_data: SpreadsheetBlockSchema = get_spreadsheet_data(spreadsheet_block=spreadsheet_block)
        education_components: list[EducationComponentSchema] = [
            EducationComponentSchema(**education_component)
            for education_component in spreadsheet_block["education_components"]
        ]

        with session_factory() as session:
            for education_component_schema in education_components:
                education_component_schema.education_component_name = education_component_schema.education_component_name.strip()
                education_component_schema.education_component_code = education_component_schema.education_component_code.strip()

                try:
                    department: DepartmentModel = session.query(DepartmentModel).filter_by(
                        department_code=education_component_schema.department
                    ).first()

                    if not department:
                        logger.warning("Department not found for")
                        continue

                    specialization: SpecializationModel = session.query(SpecializationModel).filter_by(
                        specialization_name=spreadsheet_data.specialization_name
                    ).first()

                    if not specialization:
                        logger.warning("Specialization not found for")
                        continue

                    education_component: EducationComponentModel = session.query(EducationComponentModel).filter_by(
                        education_component_code=education_component_schema.education_component_code.strip(),
                        education_component_name=education_component_schema.education_component_name.strip(),
                        education_degree=spreadsheet_data.education_degree.name,
                        department_id=department.id,
                        specialization_id=specialization.id
                    ).first()

                    if not education_component:
                        education_component: EducationComponentModel = EducationComponentModel(
                            education_component_name=education_component_schema.education_component_name.strip(),
                            education_component_code=education_component_schema.education_component_code.strip(),
                            education_degree=spreadsheet_data.education_degree.name,
                            credits=education_component_schema.credits,
                            hours=education_component_schema.hours
                        )

                        for semester_schema in education_component_schema.semesters:
                            education_component.semesters.append(create_semester_model_from_schema(
                                semester_schema=semester_schema,
                                course_study=spreadsheet_data.course_study
                            ))

                        education_component.department = department
                        education_component.specialtization = specialization

                        logger.info(f"Created education component: "
                                    f"{education_component.education_component_code} --- "
                                    f"{education_component.education_component_name}")
                    else:
                        logger.debug(f"Education component is exists: "
                                     f"{education_component.education_component_code} --- "
                                     f"{education_component.education_component_name}")

                    for group_code, number_listeners in spreadsheet_data.study_groups:
                        study_group = session.query(StudyGroupModel).filter_by(group_code=group_code).first()

                        if not study_group:
                            study_group: StudyGroupModel = StudyGroupModel(
                                group_code=group_code,
                                course_study=spreadsheet_data.course_study,
                                education_degree=spreadsheet_data.education_degree.name,
                                number_listeners=number_listeners
                            )
                            logger.info(f"Created new study group {group_code}")

                        if study_group not in education_component.study_groups:
                            education_component.study_groups.append(study_group)
                            logger.info(f"Append group {group_code} for {education_component.education_component_name}")

                    session.add(education_component)
                    session.commit()
                except Exception as err:
                    logger.error(err)
                    session.rollback()
