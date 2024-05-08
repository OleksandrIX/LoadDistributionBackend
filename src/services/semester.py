from ..schemas import SemesterSchema, SemesterCreateSchema, SemesterUpdateSchema
from ..exceptions import SemesterNotFoundException, SemesterConflictException
from ..exceptions import ConflictException
from ..utils.unit_of_work import IUnitOfWork


class SemesterService:
    @staticmethod
    async def get_semesters(uow: IUnitOfWork) -> list[SemesterSchema]:
        async with uow:
            return await uow.semesters.get_all()

    @staticmethod
    async def get_semester_by_id(uow: IUnitOfWork, semester_id) -> SemesterSchema:
        async with uow:
            semester = await uow.semesters.get_one(id=semester_id)
            if not semester:
                raise SemesterNotFoundException(semester_id)
            return semester

    @staticmethod
    async def create_semester(uow: IUnitOfWork, semester: SemesterCreateSchema) -> str:
        semester_dict = semester.model_dump()
        async with uow:
            try:
                semester: SemesterSchema = await uow.semesters.add_one(data=semester_dict)
                await uow.commit()
                return str(semester.id)
            except ConflictException:
                raise SemesterConflictException()

    @staticmethod
    async def edit_semester(uow: IUnitOfWork, semester_id: str, semester: SemesterUpdateSchema) -> SemesterSchema:
        semester_dict = semester.model_dump()
        async with uow:
            try:
                is_exists = await uow.semesters.is_exists(id=semester_id)
                if not is_exists:
                    raise SemesterNotFoundException(semester_id)
                updated_semester = await uow.semesters.edit_one(updated_data=semester_dict, id=semester_id)
                await uow.commit()
                return updated_semester
            except ConflictException:
                raise SemesterConflictException()

    @staticmethod
    async def delete_semester(uow: IUnitOfWork, semester_id: str) -> None:
        async with uow:
            is_exists = await uow.semesters.is_exists(id=semester_id)
            if not is_exists:
                raise SemesterNotFoundException(semester_id)
            await uow.semesters.delete_one(id=semester_id)
            await uow.commit()
