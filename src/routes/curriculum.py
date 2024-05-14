from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File
from fastapi_pagination import paginate
from fastapi_pagination.links import Page
from loguru import logger

from ..schemas import (CurriculumFileSchema,
                       ParsedCurriculumSchema,
                       CurriculumDataRequestSchema,
                       CurriculumDataSavedResponseSchema,
                       CurriculumSpreadsheetBlockRequestSchema)
from ..services import CurriculumService
from ..utils.dependencies import UOWDependencies, SecurityDependencies

router = APIRouter(
    prefix="/api/v1/curriculums",
    tags=["Curriculum"],
    dependencies=[SecurityDependencies]
)


@router.get("", response_model=Page[CurriculumFileSchema], status_code=200)
async def get_curriculums(
        curriculum_service: Annotated[CurriculumService, Depends(CurriculumService)]
) -> Page[CurriculumFileSchema]:
    return paginate(await curriculum_service.get_curriculum_files())


@router.post("/upload", response_model=CurriculumFileSchema, status_code=201)
async def upload_curriculum(
        curriculum_service: Annotated[CurriculumService, Depends(CurriculumService)],
        file: UploadFile = File(...),
) -> CurriculumFileSchema:
    curriculum = await curriculum_service.save_curriculum_file(file)
    logger.success(f"Uploading {curriculum.filename} successfully")
    return curriculum


@router.post("/parse", response_model=ParsedCurriculumSchema, status_code=200)
async def parse_curriculum(
        curriculum_service: Annotated[CurriculumService, Depends(CurriculumService)],
        curriculum_filename: str
) -> ParsedCurriculumSchema:
    (curriculum_file,
     curriculum_spreadsheet_blocks,
     curriculum_errors) = await curriculum_service.processing_curriculum_file(curriculum_filename)

    return ParsedCurriculumSchema(
        curriculum_file=curriculum_file,
        curriculum_spreadsheet_blocks=[CurriculumSpreadsheetBlockRequestSchema(**spreadsheet_block)
                                       for spreadsheet_block in curriculum_spreadsheet_blocks],
        curriculum_errors=curriculum_errors,
    )


@router.post("/save", response_model=CurriculumDataSavedResponseSchema, status_code=201)
async def save_curriculum_data(
        uow: UOWDependencies,
        curriculum_service: Annotated[CurriculumService, Depends(CurriculumService)],
        curriculum_data: CurriculumDataRequestSchema
) -> CurriculumDataSavedResponseSchema:
    education_components = await curriculum_service.save_curriculum_data(
        uow,
        curriculum_data.curriculum_spreadsheet_blocks
    )
    return CurriculumDataSavedResponseSchema(education_components=education_components)
