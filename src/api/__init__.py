from .curriculum import router as curriculum_router
from .file import router as file_router
from .department import router as department_router

all_routers = [
    department_router,
    curriculum_router,
    file_router
]
