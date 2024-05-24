from ..schemas import TeacherSchema, TeacherCreateSchema, TeacherUpdateSchema
from ..exceptions import TeacherNotFoundException, TeacherConflictException
from ..exceptions import ConflictException
from ..utils.dependencies import IUnitOfWork


class TeacherService:
    @staticmethod
    async def get_teachers(uow: IUnitOfWork) -> list[TeacherSchema]:
        async with uow:
            return await uow.teachers.get_all()

    @staticmethod
    async def get_teacher_by_id(uow: IUnitOfWork, teacher_id: str) -> TeacherSchema:
        async with uow:
            teacher = await uow.teachers.get_one(id=teacher_id)
            if not teacher:
                raise TeacherNotFoundException(teacher_id)
            return teacher

    @staticmethod
    async def create_teacher(uow: IUnitOfWork, teacher: TeacherCreateSchema) -> str:
        teacher_dict = teacher.model_dump()
        async with uow:
            try:
                teacher: TeacherSchema = await uow.teachers.create_one(data=teacher_dict)
                await uow.commit()
                return str(teacher.id)
            except ConflictException:
                raise TeacherConflictException()

    @staticmethod
    async def edit_teacher(uow: IUnitOfWork,
                           teacher_id: str,
                           teacher: TeacherUpdateSchema) -> TeacherSchema:
        teacher_dict = teacher.model_dump()
        async with uow:
            try:
                is_exists = await uow.teachers.is_exists(id=teacher_id)
                if not is_exists:
                    raise TeacherNotFoundException(teacher_id)
                updated_teacher = await uow.teachers.edit_one(
                    updated_data=teacher_dict,
                    id=teacher_id
                )
                await uow.commit()
                return updated_teacher
            except ConflictException:
                raise TeacherConflictException()

    @staticmethod
    async def delete_teacher(uow: IUnitOfWork, teacher_id: str) -> None:
        async with uow:
            is_exists = await uow.teachers.is_exists(id=teacher_id)
            if not is_exists:
                raise TeacherNotFoundException(teacher_id)
            await uow.teachers.delete_one(id=teacher_id)
            await uow.commit()
