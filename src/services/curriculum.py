import io

from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from loguru import logger
from minio import Minio, S3Error

from modules.curriculum_parser import processing_of_curriculum
from .calculation_academic_workload import CalculationAcademicWorkloadService
from ..config import minio_settings
from ..exceptions import CurriculumNotFoundException
from ..schemas import *
from ..utils.curriculum import (get_curriculum_spreadsheet_block_data,
                                get_current_semester_from_course_and_semester_number)
from ..utils.unit_of_work import IUnitOfWork


class CurriculumService:
    def __init__(self):
        self.minio_client = Minio(
            minio_settings.minio_url,
            access_key=minio_settings.MINIO_ACCESS_KEY,
            secret_key=minio_settings.MINIO_SECRET_KEY,
            secure=minio_settings.MINIO_SECURE
        )

        self.curriculum_dir = "curriculums/"

    async def get_curriculum_files(self) -> list[CurriculumFileSchema]:
        files: list[CurriculumFileSchema] = []
        minio_files = self.minio_client.list_objects(
            bucket_name=minio_settings.MINIO_BUCKET_NAME,
            prefix=self.curriculum_dir
        )

        for minio_file in minio_files:
            file_stat = self.minio_client.stat_object(
                bucket_name=minio_file.bucket_name,
                object_name=minio_file.object_name
            )

            files.append(CurriculumFileSchema(
                etag=file_stat.etag,
                bucket_name=file_stat.bucket_name,
                filename=file_stat.object_name.split("/")[-1],
                content_type=file_stat.content_type,
                size=file_stat.size,
            ))
        return files

    async def get_curriculum_file(self, filename: str):
        try:
            file_stat = self.minio_client.stat_object(
                bucket_name=minio_settings.MINIO_BUCKET_NAME,
                object_name=self.curriculum_dir + filename
            )

            file = self.minio_client.get_object(
                bucket_name=minio_settings.MINIO_BUCKET_NAME,
                object_name=self.curriculum_dir + filename
            )

            file_data = io.BytesIO(file.read())
            response = StreamingResponse(
                content=file_data,
                status_code=200,
                media_type=file_stat.content_type
            )

            response.headers["Content-Disposition"] = f"attachment; filename={file_stat.etag}"
            return response
        except S3Error as err:
            if err.code == "NoSuchKey":
                raise CurriculumNotFoundException(filename)
            else:
                raise Exception(err)

    async def save_curriculum_file(self, file: UploadFile) -> CurriculumFileSchema:
        file_data = await file.read()
        response = self.minio_client.put_object(
            bucket_name=minio_settings.MINIO_BUCKET_NAME,
            object_name=self.curriculum_dir + file.filename,
            data=io.BytesIO(file_data),
            length=len(file_data),
            content_type=file.content_type
        )

        file_stat = self.minio_client.stat_object(
            bucket_name=response.bucket_name,
            object_name=response.object_name
        )

        file = CurriculumFileSchema(
            etag=file_stat.etag,
            bucket_name=file_stat.bucket_name,
            filename=file_stat.object_name.split("/")[-1],
            content_type=file_stat.content_type,
            size=file_stat.size,
        )
        return file

    async def processing_curriculum_file(self, filename) -> tuple[CurriculumFileSchema, list, list]:
        try:
            file = self.minio_client.get_object(
                bucket_name=minio_settings.MINIO_BUCKET_NAME,
                object_name=self.curriculum_dir + filename
            )

            file_data = io.BytesIO(file.read())
            curriculum_spreadsheet_blocks, curriculum_errors = processing_of_curriculum(file_data, filename)
            file_stat = self.minio_client.stat_object(
                bucket_name=minio_settings.MINIO_BUCKET_NAME,
                object_name=self.curriculum_dir + filename
            )

            curriculum_file = CurriculumFileSchema(
                etag=file_stat.etag,
                bucket_name=file_stat.bucket_name,
                filename=file_stat.object_name,
                content_type=file_stat.content_type,
                size=file_stat.size,
            )

            return curriculum_file, curriculum_spreadsheet_blocks, curriculum_errors
        except S3Error as err:
            if err.code == "NoSuchKey":
                raise CurriculumNotFoundException(filename)
            else:
                raise Exception(err)

    @staticmethod
    async def save_curriculum_data(
            uow: IUnitOfWork,
            curriculum_spreadsheet_blocks: list[CurriculumSpreadsheetBlockSchema],
            data_of_years: str
    ):
        created_discipline_ids = set()
        async with uow:
            for spreadsheet_block in curriculum_spreadsheet_blocks:
                block_data = get_curriculum_spreadsheet_block_data(spreadsheet_block)
                for ec_schema in block_data.education_components:
                    department: DepartmentSchema = await uow.departments.get_one(
                        department_code=ec_schema.department)
                    specialization: SpecializationSchema = await uow.specializations.get_one(
                        specialization_name=block_data.specialization_name)

                    if not department:
                        logger.warning(f"Department with code {ec_schema.department} not found")
                        continue

                    if not specialization:
                        logger.warning(f"Specialization with name {block_data.specialization_name} not found")
                        continue

                    discipline: DisciplineSchema = await uow.disciplines.get_one(
                        discipline_name=ec_schema.education_component_name.strip(),
                        data_of_years=data_of_years,
                        department_id=department.id,
                    )

                    if not discipline:
                        discipline: DisciplineSchema = await uow.disciplines.create_one(
                            data=DisciplineCreateSchema(
                                discipline_name=ec_schema.education_component_name.strip(),
                                credits=ec_schema.credits,
                                hours=ec_schema.hours,
                                data_of_years=data_of_years,
                                department_id=department.id,
                            ).model_dump()
                        )
                        created_discipline_ids.add(discipline.id)
                        logger.success(f"Created discipline with name '{discipline.discipline_name}'")

                    education_component: EducationComponentSchema = await uow.education_components.get_one(
                        education_component_code=ec_schema.education_component_code.strip(),
                        education_degree=block_data.education_degree,
                        course_study=block_data.course_study,
                        discipline_id=str(discipline.id),
                        specialization_id=str(specialization.id)
                    )

                    if not education_component:
                        education_component: EducationComponentSchema = await uow.education_components.create_one(
                            data=EducationComponentCreateSchema(
                                education_component_code=ec_schema.education_component_code.strip(),
                                education_degree=block_data.education_degree,
                                course_study=block_data.course_study,
                                discipline_id=str(discipline.id),
                                specialization_id=str(specialization.id)
                            ).model_dump()
                        )

                        for semester_schema in ec_schema.semesters:
                            semester: SemesterSchema = await uow.semesters.create_one(
                                data=SemesterCreateSchema(
                                    semester_number=get_current_semester_from_course_and_semester_number(
                                        course=block_data.course_study,
                                        semester=semester_schema.semester_number
                                    ),
                                    total_amount_hours=semester_schema.total_amount_hours,
                                    reporting_type=semester_schema.reporting_type,
                                    education_component_id=str(education_component.id),
                                ).model_dump()
                            )

                            academic_hours = semester_schema.academic_hours
                            await uow.academic_hours.create_one(
                                data=AcademicHoursCreateSchema(
                                    amount_classroom_hours=academic_hours.amount_classroom_hours,
                                    lecture_hours=academic_hours.lecture_hours,
                                    group_hours=academic_hours.group_hours,
                                    practical_hours=academic_hours.practical_hours,
                                    self_study_hours=academic_hours.self_study_hours,
                                    semester_id=str(semester.id)
                                ).model_dump()
                            )

                            academic_task = semester_schema.academic_task
                            await uow.academic_tasks.create_one(
                                data=AcademicTaskCreateSchema(
                                    term_papers=academic_task.term_papers,
                                    modular_control_works=academic_task.modular_control_works,
                                    essays=academic_task.essays,
                                    calculation_graphic_works=academic_task.calculation_graphic_works,
                                    semester_id=str(semester.id)
                                ).model_dump()
                            )

                        logger.success(f"Created education component with id '{education_component.id}'")

                    for group_code, number_listeners in block_data.study_groups:
                        study_group: StudyGroupSchema = await uow.study_groups.get_one(group_code=group_code)

                        if not study_group:
                            study_group: StudyGroupSchema = await uow.study_groups.create_one(
                                data=StudyGroupCreateSchema(
                                    group_code=group_code,
                                    course_study=block_data.course_study,
                                    education_degree=block_data.education_degree,
                                    number_listeners=number_listeners,
                                ).model_dump()
                            )
                            logger.success(f"Created study group with id '{study_group.id}'")

                        is_exists = await uow.education_components_study_groups.is_exists(
                            education_component_id=str(education_component.id),
                            study_group_id=str(study_group.id)
                        )

                        if not is_exists:
                            await uow.education_components_study_groups.create_one(
                                data=EducationComponentsStudyGroupsSchema(
                                    education_component_id=str(education_component.id),
                                    study_group_id=str(study_group.id)
                                ).model_dump()
                            )

                    await uow.commit()

            logger.info("The end of saving data from spreadsheet")

            for discipline_id in created_discipline_ids:
                discipline = await uow.disciplines.get_one(id=discipline_id)

                calculation_workload = await CalculationAcademicWorkloadService.calculation_workload_for_discipline(
                    uow=uow,
                    discipline_id=discipline_id
                )
                logger.info(f"Calculation academic workload for discipline '{discipline.discipline_name}'")

                saved_academic_workload = await CalculationAcademicWorkloadService.save_academic_workload(
                    uow=uow,
                    academic_workload=calculation_workload
                )

                logger.info(f"Saved academic workload for discipline '{discipline.discipline_name}'")

                discipline.academic_workload_id = saved_academic_workload.id
                await uow.disciplines.edit_one(
                    updated_data=DisciplineSchema(**discipline.model_dump()).model_dump(),
                    id=discipline.id
                )
                logger.success(f"Added academic workload for discipline: {discipline.discipline_name}")
                await uow.commit()

    async def delete_curriculum_file(self, filename: str):
        try:
            self.minio_client.remove_object(
                bucket_name=minio_settings.MINIO_BUCKET_NAME,
                object_name=self.curriculum_dir + filename
            )
        except S3Error as err:
            if err.code == "NoSuchKey":
                raise CurriculumNotFoundException(filename)
            else:
                raise Exception(err)
