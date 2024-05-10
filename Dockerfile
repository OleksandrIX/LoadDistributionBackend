FROM python:3.11-slim

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /app
ADD pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY . .
