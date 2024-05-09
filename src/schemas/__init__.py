from .curriculum import (CurriculumFileSchema,
                         ParsedCurriculumSchema,
                         CurriculumDataRequestSchema,
                         CurriculumSpreadsheetBlockRequestSchema,
                         CurriculumSpreadsheetBlockSchema,
                         CurriculumEducationComponentSchema,
                         CurriculumDataSavedResponseSchema)
from .department import (DepartmentSchema,
                         DepartmentCreateSchema,
                         DepartmentUpdateSchema)
from .specialty import (SpecialtySchema,
                        SpecialtyCreateSchema,
                        SpecialtyUpdateSchema)
from .specialization import (SpecializationSchema,
                             SpecializationCreateSchema,
                             SpecializationUpdateSchema)
from .education_component import (EducationComponentSchema,
                                  EducationComponentCreateSchema,
                                  EducationComponentUpdateSchema)
from .study_group import (StudyGroupSchema,
                          StudyGroupCreateSchema,
                          StudyGroupUpdateSchema)
from .semester import (SemesterSchema,
                       SemesterCreateSchema,
                       SemesterUpdateSchema)
from .academic_hours import (AcademicHoursSchema,
                             AcademicHoursCreateSchema,
                             AcademicHoursUpdateSchema)
from .academic_task import (AcademicTaskSchema,
                            AcademicTaskCreateSchema,
                            AcademicTaskUpdateSchema)
from .education_components_study_groups import EducationComponentsStudyGroupsSchema
from .user import UserSchema, UserRegistrationSchema, UserLoginSchema, TokenSchema, TokenPayload
