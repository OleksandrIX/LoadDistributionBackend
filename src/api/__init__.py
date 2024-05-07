from .department import router as department_router
from .specialty import router as specialty_router
from .specialization import router as specialization_router
from .education_component import router as education_component_router
from .study_group import router as study_group_router
from .semester import router as semester_router
from .academic_hours import router as academic_hours_router
from .academic_task import router as academic_task_router

from .curriculum import router as curriculum_router
from .file import router as file_router

all_routers = [
    department_router,
    specialty_router,
    specialization_router,
    education_component_router,
    study_group_router,
    semester_router,
    academic_hours_router,
    academic_task_router,

    curriculum_router,
    file_router
]
