import io

from minio import Minio
from loguru import logger
from fastapi import APIRouter, UploadFile, File

from ..config import minio_settings
from ..schemas import FileSchema

router = APIRouter(
    prefix="/api/v1/files",
    tags=["Upload files"]
)

minio_client = Minio(
    minio_settings.minio_url,
    access_key=minio_settings.MINIO_ACCESS_KEY,
    secret_key=minio_settings.MINIO_SECRET_KEY,
    secure=minio_settings.MINIO_SECURE
)


@router.get("", response_model=list[FileSchema], status_code=200)
async def get_files() -> list[FileSchema]:
    files: list[FileSchema] = []
    minio_files = minio_client.list_objects(bucket_name=minio_settings.MINIO_BUCKET_NAME)
    for minio_file in minio_files:
        file_stat = minio_client.stat_object(bucket_name=minio_file.bucket_name, object_name=minio_file.object_name)
        files.append(FileSchema(
            bucket_name=file_stat.bucket_name,
            filename=file_stat.object_name,
            content_type=file_stat.content_type,
            size=file_stat.size,
        ))
    return files


@router.post("/upload", response_model=FileSchema, status_code=201)
async def upload_file(file: UploadFile = File(...)) -> FileSchema:
    file_data = await file.read()
    response = minio_client.put_object(
        bucket_name=minio_settings.MINIO_BUCKET_NAME,
        object_name=file.filename,
        data=io.BytesIO(file_data),
        length=len(file_data),
        content_type=file.content_type
    )

    file_stat = minio_client.stat_object(bucket_name=response.bucket_name, object_name=response.object_name)
    file = FileSchema(
        bucket_name=file_stat.bucket_name,
        filename=file_stat.object_name,
        content_type=file_stat.content_type,
        size=file_stat.size,
    )

    logger.success(f"Uploading {file.filename} successfully")
    return file

# async def proccesing_curriculum(path_to_file: str):
#     import modules.excel_parser as excel_parser
#
#     response = {}
#
#     spreadsheets_data, errors = excel_parser.processing_of_spreadsheet(path_to_file)
#     logger.debug(f"{errors=}")
#
#     await excel_parser.processing_spreadsheet_data(spreadsheets_data)
#     logger.success(f"File {path_to_file} processed")
#
#     response[os.path.basename(path_to_file)] = {
#         "curriculum_data": spreadsheets_data,
#         "curriculum_errors": errors
#     }
#
#     return response
#
#
# async def proccesing_curriculums():
#     import modules.excel_parser as excel_parser
#
#     response = {}
#
#     paths = [
#         "example/data/excel/bachelor/RPND-bachelor.xlsx",
#         "example/data/excel/magistracy/RPND-magistracy.xlsx"
#     ]
#
#     tasks = []
#     for path in paths:
#         tasks.append(asyncio.create_task(proccesing_curriculum(path)))
#
#     results = await asyncio.gather(*tasks)
#
#     for result in results:
#         response.update(result)
#
#     return response
