from fastapi import APIRouter
from loguru import logger

router = APIRouter(
    prefix="/api/v1/curriculums",
    tags=["Curriculum"]
)


@router.get("/start")
async def start_processing_curriculum():
    logger.info("Started parsing curriculums")
    response = await proccesing_curriculums()
    return response


@router.get("")
async def get_currcilum():
    logger.info("Get curriculums")
    logger.info("Get curriculums")
    return {"curriculum": "curriculum"}
