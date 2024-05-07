from .department import router as department_router
from .specialty import router as specialty_router
from .specialization import router as specialization_router

from .curriculum import router as curriculum_router
from .file import router as file_router

all_routers = [
    department_router,
    specialty_router,
    specialization_router,
    curriculum_router,
    file_router
]
