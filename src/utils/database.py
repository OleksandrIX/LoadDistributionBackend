from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine

from ..config import database_settings

psql_engine: AsyncEngine = create_async_engine(url=database_settings.database_url, echo=False)
async_session_maker = async_sessionmaker(bind=psql_engine, autoflush=False, expire_on_commit=False)


class LoadDistributionBase(DeclarativeBase):
    metadata = MetaData("load_distribution")

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        columns = []
        for idx, column in enumerate(self.__table__.columns.keys()):
            if column in self.repr_cols or idx < self.repr_cols_num:
                columns.append(f"{column}={getattr(self, column)}")

        return f"<{self.__class__.__name__} {', '.join(columns)}>"
