from .curriculum import router as curriculum_router
from .file import router as file_router
from .department import router as department_router
from .specialization import router as specialization_router

all_routers = [
    department_router,
    specialization_router,
    curriculum_router,
    file_router
]
