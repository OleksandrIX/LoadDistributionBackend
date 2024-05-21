from ..schemas import CurriculumSpreadsheetBlockSchema, CurriculumSpreadsheetBlockRequestSchema


def get_current_semester_from_course_and_semester_number(course: int, semester: int) -> int:
    """Function to get the current semester from course number and semester number"""
    return semester + (course - 1) * 2


def get_curriculum_spreadsheet_block_data(
        spreadsheet_block: CurriculumSpreadsheetBlockRequestSchema
) -> CurriculumSpreadsheetBlockSchema:
    """Function to get the spreadsheet data from the spreadsheet block"""
    curriculum_spreadsheet_block = CurriculumSpreadsheetBlockSchema(
        specialty_code=int(str(spreadsheet_block.specialty).split()[0].strip()),
        specialization_name=str(spreadsheet_block.specialization).strip(),
        course_study=int(spreadsheet_block.course_study),
        education_degree=spreadsheet_block.education_degree,
        education_components=spreadsheet_block.education_components
    )

    for group in str(spreadsheet_block.study_groups).split(","):
        separated_groups: list[str] = group.strip().split()
        group_number: str = str(separated_groups[0].strip())
        number_listeners: int = int(separated_groups[-1]
                                    .strip()
                                    .replace("(", "")
                                    .replace(")", ""))
        curriculum_spreadsheet_block.study_groups.append((group_number, number_listeners))

    return curriculum_spreadsheet_block
