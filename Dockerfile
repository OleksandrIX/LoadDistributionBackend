FROM python:3.11-buster
WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3-dev

RUN pip install --upgrade pip
RUN pip install poetry
ADD pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

EXPOSE 8000

COPY . .

CMD ["uvicorn", "--factory", "src.main:create_app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
