from .academic_hours import (AcademicHoursSchema,
                             AcademicHoursCreateSchema,
                             AcademicHoursUpdateSchema)
from .academic_task import (AcademicTaskSchema,
                            AcademicTaskCreateSchema,
                            AcademicTaskUpdateSchema)
from .academic_workload import (AcademicWorkloadSchema,
                                AcademicWorkloadCreateSchema,
                                AcademicWorkloadUpdateSchema)
from .academic_workload_formula import (WorkloadFormulaSchema,
                                        WorkloadFormulaCreateSchema,
                                        WorkloadFormulaUpdateSchema)
from .academic_workload_teacher import (AcademicWorkloadTeacherSchema,
                                        AcademicWorkloadTeacherCreateSchema,
                                        AcademicWorkloadTeacherUpdateSchema)
from .curriculum import (CurriculumFileSchema,
                         ParsedCurriculumSchema,
                         CurriculumDataRequestSchema,
                         CurriculumSpreadsheetBlockRequestSchema,
                         CurriculumSpreadsheetBlockSchema,
                         CurriculumEducationComponentSchema,
                         CurriculumDataSavedResponseSchema)
from .department import (DepartmentSchema,
                         DepartmentCreateSchema,
                         DepartmentUpdateSchema,
                         DepartmentWithTeachersSchema,
                         DepartmentWithDisciplines,
                         DepartmentWithRelationships)
from .discipline import (DisciplineSchema,
                         DisciplineCreateSchema,
                         DisciplineUpdateSchema,
                         DisciplineWithRelationships)
from .education_component import (EducationComponentSchema,
                                  EducationComponentCreateSchema,
                                  EducationComponentUpdateSchema,
                                  EducationComponenWithWorkloadSchema,
                                  ECWithAcademicDataSchema,
                                  EducationComponentWithRelationships)
from .education_components_study_groups import EducationComponentsStudyGroupsSchema
from .semester import (SemesterSchema,
                       SemesterCreateSchema,
                       SemesterUpdateSchema,
                       SemesterWithAcademicDataSchema)
from .specialization import (SpecializationSchema,
                             SpecializationCreateSchema,
                             SpecializationUpdateSchema)
from .specialty import (SpecialtySchema,
                        SpecialtyCreateSchema,
                        SpecialtyUpdateSchema)
from .study_group import (StudyGroupSchema,
                          StudyGroupCreateSchema,
                          StudyGroupUpdateSchema)
from .teacher import (TeacherSchema,
                      TeacherCreateSchema,
                      TeacherUpdateSchema)
from .token import TokenPayloadSchema, TokenSchema
from .user import UserSchema, UserWithoutPasswordSchema, UserRegistrationSchema, UserLoginSchema
