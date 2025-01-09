from enum import Enum


class NewsStatus(Enum):
    """
    Статус новости в базе данных.
    """

    UNSEEN: str = "uns"
    FAVORITE: str = "fav"


class UserRole(Enum):
    """
    Роли для пользователя в базе данных.
    """

    USER: str = "user"
    MAIN_ADMIN: str = "main"
    ADMIN: str = "admin"
    BANNED: str = "banned"
