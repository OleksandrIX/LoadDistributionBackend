import uuid
from sqlalchemy import Column, UUID, TIMESTAMP, func
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class IdMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


@declarative_mixin
class TimestampMixin:
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now())


role_enum_args = ["USER", "ADMIN"]
academic_rank_enum_args = ["Старший науковий співробітник", "Доцент", "Професор"]
education_degree_enum_agrs = ["бакалавр", "магістр"]
reporting_type_enum_args = ["Диференційований залік", "Екзамен"]
scientific_degree_enum_args = ["Кандидат наук", "Доктор наук"]
position_enum_args = [
    "Начальник кафедри", "Заступник начальника кафедри", "Професор", "Доцент", "Старший викладач", "Викладач",
    "Асистент", "Сержант-інструктор"
]
milittary_rank_enum_args = [
    "Солдат", "Старший солдат", "Молодший сержант", "Сержант", "Старший сержант", "Головний сержант", "Штаб-сержант",
    "Майстер-сержант", "Старший майстер-сержант", "Головний майстер-сержант", "Молодший лейтенант", "Лейтенант",
    "Старший лейтенант", "Капітан", "Майор", "Підполковник", "Полковник", "Бригадний генерал", "Генерал-майор",
    "Генерал-лейтенант", "Генерал"
]
