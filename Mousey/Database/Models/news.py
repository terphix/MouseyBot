from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from Mousey.Misc import NewsStatus

from .base import Base


class News(Base):
    """
        Схема для хранения информации о предложенных новостях в БД.
    """
    __tablename__ = "news"
    
    # Уникальный ID новости
    news_id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    
    # Информация о пользователе, который предложил новость
    tg_id: Mapped[int] = mapped_column(nullable=False)
    tg_username: Mapped[str] = mapped_column(String(32), nullable=True)

    # Текст новости и контакты для связи
    text: Mapped[str] = mapped_column(Text, nullable=False)
    contact: Mapped[str] = mapped_column(Text, nullable=True)

    # Статус новости
    status: Mapped[str] = mapped_column(String(3), default=NewsStatus.UNSEEN.value, nullable=False)

