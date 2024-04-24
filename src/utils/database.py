from sqlalchemy import create_engine, Engine, MetaData
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.config.environment import database_settings

psql_engine: Engine = create_engine(url=database_settings.database_url, echo=False)
session_factory = sessionmaker(bind=psql_engine, autoflush=False)


class Base(DeclarativeBase):
    metadata = MetaData("load_distribution")
    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        columns = []
        for idx, column in enumerate(self.__table__.columns.keys()):
            if column in self.repr_cols or idx < self.repr_cols_num:
                columns.append(f"{column}={getattr(self, column)}")

        return f"<{self.__class__.__name__} {', '.join(columns)}>"
