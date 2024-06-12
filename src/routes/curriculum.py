from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import StreamingResponse
from loguru import logger

from ..schemas import (CurriculumFileSchema,
                       ParsedCurriculumSchema,
                       CurriculumDataRequestSchema,
                       CurriculumDataSavedResponseSchema,
                       CurriculumSpreadsheetBlockRequestSchema)
from ..services import CurriculumService
from ..utils.dependencies import UOWDependencies, SecurityDependencies, AdminDependencies
from ..utils.file_extensions import check_curriculm_file_extension

CurriculumServiceDependencies = Annotated[CurriculumService, Depends(CurriculumService)]
router = APIRouter(
    prefix="/api/v1/curriculums",
    tags=["Curriculum"],
    dependencies=[SecurityDependencies]
)


@router.get(
    "",
    response_model=list[CurriculumFileSchema],
    status_code=200,
    dependencies=[AdminDependencies]
)
async def get_curriculums(
        curriculum_service: CurriculumServiceDependencies
) -> list[CurriculumFileSchema]:
    return await curriculum_service.get_curriculum_files()


@router.post(
    path="/upload",
    response_model=CurriculumFileSchema,
    status_code=201,
    dependencies=[AdminDependencies]
)
async def upload_curriculum(
        curriculum_service: CurriculumServiceDependencies,
        file: UploadFile = File(...),
) -> CurriculumFileSchema:
    check_curriculm_file_extension(file.filename)
    curriculum = await curriculum_service.save_curriculum_file(file)
    logger.success(f"Uploading {curriculum.filename} successfully")
    return curriculum


@router.get(
    path="/download",
    status_code=200,
    dependencies=[AdminDependencies]
)
async def download_curriculum(
        curriculum_service: CurriculumServiceDependencies,
        curriculum_filename: str
) -> StreamingResponse:
    check_curriculm_file_extension(curriculum_filename)
    return await curriculum_service.get_curriculum_file(curriculum_filename)


@router.post(
    path="/parse",
    response_model=ParsedCurriculumSchema,
    status_code=200,
    dependencies=[AdminDependencies]
)
async def parse_curriculum(
        curriculum_service: CurriculumServiceDependencies,
        curriculum_filename: str
) -> ParsedCurriculumSchema:
    check_curriculm_file_extension(curriculum_filename)
    (curriculum_file,
     curriculum_spreadsheet_blocks,
     curriculum_errors) = await curriculum_service.processing_curriculum_file(curriculum_filename)

    return ParsedCurriculumSchema(
        curriculum_file=curriculum_file,
        curriculum_spreadsheet_blocks=[CurriculumSpreadsheetBlockRequestSchema(**spreadsheet_block)
                                       for spreadsheet_block in curriculum_spreadsheet_blocks],
        curriculum_errors=curriculum_errors,
    )


@router.post(
    path="/save",
    response_model=None,
    status_code=201,
    dependencies=[AdminDependencies]
)
async def save_curriculum_data(
        uow: UOWDependencies,
        curriculum_service: CurriculumServiceDependencies,
        curriculum_data: CurriculumDataRequestSchema,
        data_of_years: str
) -> CurriculumDataSavedResponseSchema:
    await curriculum_service.save_curriculum_data(uow, curriculum_data.curriculum_spreadsheet_blocks, data_of_years)


@router.delete(
    path="",
    response_model=None,
    status_code=204,
    dependencies=[AdminDependencies]
)
async def delete_curriculum(
        curriculum_service: CurriculumServiceDependencies,
        curriculum_filename: str
) -> None:
    check_curriculm_file_extension(curriculum_filename)
    await curriculum_service.delete_curriculum_file(curriculum_filename)
    logger.success(f"Deleted curriculum file with filename '{curriculum_filename}'")
