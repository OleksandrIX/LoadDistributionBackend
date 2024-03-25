import os
import psycopg2
from loguru import logger
import time


class PostgreSQLDatabase:
    def __init__(self, host="localhost", port="5432", database="postgres", user="postgres", password="postgres"):
        self.host = os.environ.get("DB_HOST") or host
        self.port = os.environ.get("DB_PORT") or port
        self.database_name = os.environ.get("DB_NAME") or database
        self.user = os.environ.get("DB_USER") or user
        self.password = os.environ.get("DB_PASSWORD") or password
        self.connection = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        self.connection = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database_name,
            user=self.user,
            password=self.password
        )
        return self.connection

    def close(self):
        self.connection.close()

    def execute(self, query, parameters=()):
        cursor = self.connection.cursor()
        cursor.execute(query, parameters)
        return cursor

    def fetch_one(self, query, parameters=()):
        return self.execute(query, parameters).fetchone()

    def fetch_all(self, query, parameters=()):
        return self.execute(query, parameters).fetchall()


def validation_database_connect():
    connection = None
    try:
        logger.trace("Connecting to the PostgreSQL database...")
        connection = PostgreSQLDatabase().connect()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.exception(error)
    finally:
        if connection is not None:
            logger.info("Connection to the PostgreSQL database successful.")
            return connection
        else:
            logger.error("Connection to the PostgreSQL database failed.")
