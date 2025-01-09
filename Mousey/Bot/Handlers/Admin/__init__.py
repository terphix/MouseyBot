__all__ = ["__setup_admin_router"]

from loguru import logger

from aiogram import Router, F
from aiogram.filters import Command

from Mousey.Misc import UserRole
from Mousey.Bot.Filters import UserRoleFilter

from .info import cmd_admin_database_info
from .utils import (
    cmd_sticker_id,
    cmd_update_role,
)
from .menu import (
    cmd_admin_menu,
    call_admin_menu,
    call_admin_commands,
)
from .news import (
    call_news_menu,
    call_news_favorite,
    call_news_offer_menu,
)


def __setup_admin_router() -> Router:
    """
        Регистрация событий для роутера администрации бота.
    """
    router = Router()

    ############
    ### Меню ###
    ############
    router.message.register(cmd_admin_menu, Command("admin"))
    router.callback_query.register(call_admin_menu, F.data == "admin_menu")

    router.callback_query.register(call_admin_commands, F.data == "admin_commands")

    #######################
    ### Сбор информации ###
    #######################
    router.message.register(cmd_admin_database_info, Command("database_info"))
    
    ##############
    ### Разное ###
    ##############
    router.message.register(cmd_sticker_id, F.sticker)
    router.message.register(
        cmd_update_role,
        Command("update_role"),
        UserRoleFilter(UserRole.MAIN_ADMIN),
    )

    ##########################
    ### Модерация новостей ###
    ##########################
    router.callback_query.register(call_news_menu, F.data == "admin_news_menu")
    router.callback_query.register(
        call_news_favorite,
        F.data == "admin_news_favorite",
    )
    
    # Просмотр новостей
    router.callback_query.register(
        call_news_offer_menu,
        F.data.startswith("admin_news_offer_"),
    )

    logger.success("Роутер для модерации готов.")
    
    # Вывод роутера
    return router

