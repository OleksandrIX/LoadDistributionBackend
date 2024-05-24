from abc import ABC, abstractmethod

from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..exceptions import ConflictException


class AbstractRepository(ABC):
    @abstractmethod
    async def is_exists(self, **filter_by):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, **filter_by):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, **filter_by):
        raise NotImplementedError

    @abstractmethod
    async def create_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, data: dict, **filter_by):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, **filter_by):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def is_exists(self, **filter_by) -> bool:
        """
        Checks if the entity exist by filters in table.
        :param filter_by: filters by which you want to check a table entry
        :return: True if existed, False if not existed
        """
        try:
            query = select(self.model).filter_by(**filter_by)
            result = await self.session.execute(query)
            return bool(result.scalar_one())
        except NoResultFound:
            return False

    async def get_one(self, **filter_by) -> model:
        """
        Returns the entity by filters in table.
        :param filter_by: filters by which you want to check a table entry
        :return: entity instance
        """
        try:
            query = select(self.model).filter_by(**filter_by)
            result = await self.session.execute(query)
            return result.scalar_one().to_read_model()
        except NoResultFound:
            return None

    async def get_all(self, **filter_by) -> list[model]:
        """
        Returns all entities in the table.
        :return: list of entities
        """
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        entities = result.scalars().all()
        return [row.to_read_model() for row in entities]

    async def create_one(self, data: dict) -> str:
        """
        Adds a new entity in the table.
        :param data: dictionary with data to be added into the table
        :return: entity id
        """
        try:
            stmt = insert(self.model).values(**data).returning(self.model)
            result = await self.session.execute(stmt)
            return result.scalar_one().to_read_model()
        except IntegrityError:
            raise ConflictException()

    async def edit_one(self, updated_data: dict, **filter_by) -> model:
        """
        Updates the entity by filters in table.
        :param updated_data: dictionary with data to be updated into the table
        :param filter_by: filters by which you want to check a table entry
        :return: entity instance
        """
        try:
            stmt = update(self.model).filter_by(**filter_by).values(**updated_data).returning(self.model)
            result = await self.session.execute(stmt)
            return result.scalar_one().to_read_model()
        except IntegrityError:
            raise ConflictException()

    async def delete_one(self, **filter_by) -> None:
        """
        Deletes the entity by filters in table.
        :param filter_by: filters by which you want to check a table entry
        """
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
