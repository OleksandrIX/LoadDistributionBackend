from pydantic import BaseModel
from fastapi import File, UploadFile


class FileSchema(BaseModel):
    bucket_name: str
    filename: str
    content_type: str
    size: int
