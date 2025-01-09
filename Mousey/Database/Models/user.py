from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

from Mousey.Misc import UserRole


class Users(Base):
    """
        Схема для хранения информации о пользователях бота в БД.
    """
    __tablename__ = "user"
    
    # Уникальный ID пользователя (Telegram ID)
    tg_id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=False)

    # Статистика по новостям у пользователя
    all_news: Mapped[int] = mapped_column(default=0, nullable=False)
    unseen_news: Mapped[int] = mapped_column(default=0, nullable=False)
    
    # Роль пользователя для бота
    role: Mapped[str] = mapped_column(String(16), default=UserRole.USER.value, nullable=False)

