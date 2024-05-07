# Load Distribution API

### _Step by step:_

First, you need to create 4 files in the environments directory, namely:

- **.env.application** - it stores values about the application
  (it includes: version and name)
- **.env.logger** - it stores the values for creating a logger 
  (it includes: the directory where the files will be stored, log level, rotation and compression)
- **.env.database** - it stores the values for connection to database 
  (it includes: host, port, user, password and database name)
- **.env.minio** - it stores the values for connection to MinIO service 
  (it includes: host, port, access and secret keys, bucket name and whether the connection is secure)

The next thing to do is to execute the following command:

```shell
poetry install --no-root
```



### _Folder structure:_

```text
.
├── Dockerfile
├── environments
│   ├── .env.application
│   ├── .env.application
    ├── .env.application
    ├── .env.application
│   └── example.env
├── logs
│   └── load-distribution-api-v0.1.1.log
├── modules
│   └── excel_parser
│       ├── __init__.py
│       ├── exceptions
│       │         └── ParsingException.py
│       ├── read_spreadsheet.py
│       ├── save_spreadsheet_data.py
│       ├── spreadsheet_schemas.py
│       └── utils
│           ├── dataframe_utils.py
│           ├── data_utils.py
│           └── spreadsheet_utils.py
├── poetry.lock
├── pyproject.toml
├── README.md
└── src
    ├── api
    │         ├── __init__.py
    │         ├── curriculum.py
    │         ├── department.py
    │         └── file.py
    ├── config
    │         ├── __init__.py
    │         ├── environment.py
    │         └── logger.py
    ├── exceptions
    │         ├── __init__.py
    │         ├── conflict.py
    │         └── not_found.py
    ├── main.py
    ├── middlewares
    │         ├── __init__.py
    │         └── exception.py
    ├── models
    │         ├── __init__.py
    │         ├── academic_hours.py
    │         ├── academic_task.py
    │         ├── department.py
    │         ├── education_component.py
    │         ├── many_to_many_tables.py
    │         ├── semester.py
    │         ├── specialization.py
    │         ├── specialty.py
    │         └── study_group.py
    ├── repositories
    │         ├── __init__.py
    │         ├── academic_hours.py
    │         ├── academic_task.py
    │         ├── department.py
    │         ├── education_component.py
    │         ├── semester.py
    │         ├── specialization.py
    │         ├── specialty.py
    │         └── study_group.py
    ├── schemas
    │         ├── __init__.py
    │         ├── department.py
    │         └── file.py
    ├── services
    │         ├── __init__.py
    │         └── department.py
    └── utils
        ├── database.py
        ├── dependencies.py
        ├── model.py
        ├── repository.py
        ├── schema.py
        └── unit_of_work.py
```