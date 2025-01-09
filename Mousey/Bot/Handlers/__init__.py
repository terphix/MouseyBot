__all__ = ["setup_routers"]

from aiogram import Router

from .Admin import __setup_admin_router
from .Private import __setup_private_router

from Mousey.Misc import UserRole
from Mousey.Bot.Filters import add_filters, ChatTypeFilter, UserRoleFilter


def setup_routers(dispatcher: Router) -> None:
    """
        Настройка всех роутеров и подключение их к диспетчеру.
    """
    # Пользовательский роутер для ЛС бота
    private_router = __setup_private_router()
    add_filters(
        private_router,
        "all",
        ChatTypeFilter("private"),
    )

    # Роутер для администрации
    admin_router = __setup_admin_router()
    add_filters(
        admin_router,
        "all",
        ChatTypeFilter("private"),
        UserRoleFilter(
            user_role=[
                UserRole.ADMIN,
                UserRole.MAIN_ADMIN,
            ],
        ),
    )

    dispatcher.include_routers(
        private_router,
        admin_router,
    )

