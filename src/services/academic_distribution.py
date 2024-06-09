import json
from datetime import datetime
from io import BytesIO

from loguru import logger
from minio import Minio, S3Error

from ..config import minio_settings
from ..exceptions import NotFoundException


class AcademicDistributionService:
    def __init__(self):
        self.minio_client = Minio(
            minio_settings.minio_url,
            access_key=minio_settings.MINIO_ACCESS_KEY,
            secret_key=minio_settings.MINIO_SECRET_KEY,
            secure=minio_settings.MINIO_SECURE
        )

        self.curriculum_dir = "distribution-sessions/"

    async def get_all_sessions(self, department_code: str):
        sessions = []
        prefix = f"{self.curriculum_dir}{department_code}/"

        objects = self.minio_client.list_objects(minio_settings.MINIO_BUCKET_NAME, prefix=prefix, recursive=True)
        for obj in objects:
            sessions.append(obj.object_name.split("/")[-1].replace(".json", ""))
        return sessions

    async def get_session(self, department_code: str, distribution_name: str):
        file_path = f"{self.curriculum_dir}{department_code}/{distribution_name}.json"

        try:
            response = self.minio_client.get_object(minio_settings.MINIO_BUCKET_NAME, file_path)
            session_data = json.load(response)
            response.close()
            response.release_conn()
            return session_data
        except S3Error:
            raise NotFoundException(message="Session not found")

    async def save_session(self, department_code: str, session_data: dict):
        distribution_name = session_data.get("distribution_name", datetime.now().strftime("%Y%m%d%H%M%S"))
        file_path = f"{self.curriculum_dir}{department_code}/{distribution_name}.json"

        session_json = json.dumps(session_data)

        try:
            self.minio_client.put_object(
                bucket_name=minio_settings.MINIO_BUCKET_NAME,
                object_name=file_path,
                data=BytesIO(session_json.encode("utf-8")),
                length=len(session_json),
                content_type="application/json"
            )
        except S3Error as error:
            logger.error(error)

    async def delete_session(self, department_code: str, distribution_name: str):
        file_path = f"{self.curriculum_dir}{department_code}/{distribution_name}.json"

        try:
            self.minio_client.remove_object(minio_settings.MINIO_BUCKET_NAME, file_path)
        except S3Error as err:
            if err.code == "NoSuchKey":
                raise NotFoundException(message=f"Session '{file_path}' not found")
            else:
                raise Exception(err)
