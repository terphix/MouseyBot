from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
        Основной шаблон для схем в базе данных.
    """
    # Информация о том, когда была добавлена строка в БД
    added: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    # Информация о том, когда последний раз была обновлена строчка
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

