import datetime

from sqlalchemy import BigInteger, SmallInteger, DateTime, func, String, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.api.schemas.user import Role


class User(Base):  # обязательно наследуем все модели от нашей Base-метатаблицы
    __tablename__ = "users"  # Указываем как будет называться наша таблица в базе данных (пишется в ед. числе)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)  # Строка  говорит, что наша колонка будет интом, но уточняет, что ещё и большим интом (актуально для ТГ-ботов), первичным ключом и индексироваться
    login: Mapped[str]  = mapped_column(String, nullable=False, unique=True)
    name: Mapped[str]  = mapped_column(String, nullable=True)
    surname: Mapped[str] = mapped_column(String, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=True)
    roles: Mapped[tuple[Role]] = mapped_column(ARRAY(SmallInteger), as_tuple=True)
    logged: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
