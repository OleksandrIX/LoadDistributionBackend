from uuid import UUID
from enum import Enum
from datetime import datetime
from pydantic import BaseModel


class IdMixinSchema(BaseModel):
    id: UUID


class TimestampMixinSchema(BaseModel):
    created_at: datetime
    updated_at: datetime


class EducationDegreeEnum(str, Enum):
    bachelor = "бакалавр"
    master = "магістр"


class ReportingTypeEnum(str, Enum):
    graded_test = "Диференційований залік"
    exam = "Екзамен"


class PositionEnum(str, Enum):
    HEAD_OF_THE_DEPARTMENT = "Начальник кафедри"
    DEPUTY_HEAD_OF_THE_DEPARTMENT = "Заступник начальника кафедри"
    PROFESSOR = "Професор"
    ASSOCIATE_PROFESSOR = "Доцент"
    SENIOR_LECTURER = "Старший викладач"
    LECTURER = "Викладач"
    ASSISTANT = "Асистент"
    SERGEANT_INSTRUCTOR = "Сержант-інструктор"


class MilitaryRankEnum(str, Enum):
    SOLDIER = "Солдат"
    SENIOR_SOLDIER = "Старший солдат"
    JUNIOR_SERGEANT = "Молодший сержант"
    SERGEANT = "Сержант"
    SENIOR_SERGEANT = "Старший сержант"
    CHIEF_SERGEANT = "Головний сержант"
    STAFF_SERGEANT = "Штаб-сержант"
    MASTER_SERGEANT = "Майстер-сержант"
    SENIOR_MASTER_SERGEANT = "Старший майстер-сержант"
    CHIEF_MASTER_SERGEANT = "Головний майстер-сержант"
    JUNIOR_LIEUTENANT = "Молодший лейтенант"
    LIEUTENANT = "Лейтенант"
    SENIOR_LIEUTENANT = "Старший лейтенант"
    CAPTAIN = "Капітан"
    MAJOR = "Майор"
    LIEUTENANT_COLONEL = "Підполковник"
    COLONEL = "Полковник"
    BRIGADIER_GENERAL = "Бригадний генерал"
    MAJOR_GENERAL = "Генерал-майор"
    LIEUTENANT_GENERAL = "Генерал-лейтенант"
    GENERAL = "Генерал"


class AcademicRankEnum(str, Enum):
    SENIOR_RESEARCHER = "Старший науковий співробітник"
    ASSOCIATE_PROFESSOR = "Доцент"
    PROFESSOR = "Професор"


class ScientificDegreeEnum(str, Enum):
    CANDIDATE_OF_SCIENCE = "Кандидат наук"
    DOCTOR_OF_SCIENCE = "Доктор наук"
