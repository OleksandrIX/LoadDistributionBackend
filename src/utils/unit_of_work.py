from typing import Type
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from ..repositories import *
from .database import async_session_maker


class IUnitOfWork(ABC):
    departments: Type[DepartmentRepository]
    specialties: Type[SpecialtyRepository]
    specializations: Type[SpecializationRepository]
    education_components: Type[EducationComponentRepository]
    study_groups: Type[StudyGroupRepository]
    semesters: Type[SemesterRepository]
    academic_hours: Type[AcademicHoursRepository]
    academic_tasks: Type[AcademicTaskRepository]
    education_components_study_groups: Type[EducationComponentsStudyGroupsRepository]

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:

    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()

        self.departments = DepartmentRepository(self.session)
        self.specialties = SpecialtyRepository(self.session)
        self.specializations = SpecializationRepository(self.session)
        self.education_components = EducationComponentRepository(self.session)
        self.study_groups = StudyGroupRepository(self.session)
        self.semesters = SemesterRepository(self.session)
        self.academic_hours = AcademicHoursRepository(self.session)
        self.academic_tasks = AcademicTaskRepository(self.session)
        self.education_components_study_groups = EducationComponentsStudyGroupsRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
