__all__ = ["__setup_private_router"]

from loguru import logger

from aiogram import Router, F
from aiogram.filters import Command

from Mousey.Bot.States import OfferNews

from .utils import cmd_get_stickers, cmd_cancel
from .menu import cmd_menu, call_menu, call_useful_info, call_about_bot_info
from .news import (
    call_news_menu,
    cmd_news_offer,
    call_news_offer,
    call_input_news_text,
    call_news_offer_send,
    call_news_statistics,
    cmd_news_input_error,
    call_news_offer_cancel,
    call_input_news_contact,
)


def __setup_private_router() -> Router:
    """
        Регистрация событий для роутера пользователей.
    """
    router = Router()

    ########################
    ### Полезные команды ###
    ########################
    router.message.register(cmd_cancel, Command("cancel"))
    router.message.register(cmd_get_stickers, Command("get_stickers"))
    
    #########################
    ### Главное меню бота ###
    #########################
    router.message.register(cmd_menu, Command(commands=["start", "menu"]))
    router.callback_query.register(call_menu, F.data == "menu")

    router.callback_query.register(call_useful_info, F.data == "useful_info")
    router.callback_query.register(call_about_bot_info, F.data == "about_bot_info")

    ######################
    ### Новостное меню ###
    ######################
    router.callback_query.register(call_news_menu, F.data == "news_menu")
    
    # Статистика новостей
    router.callback_query.register(call_news_statistics, F.data == "news_statistics")
    
    # Меню, для предложки новостей
    router.callback_query.register(call_news_offer, F.data == "news_offer")

    # Кнопки при предложении новости
    router.callback_query.register(call_input_news_text, F.data == "news_input_text")
    router.callback_query.register(call_input_news_contact, F.data == "news_input_contact")

    # Обработка ввода текста для предложки
    router.message.register(
        cmd_news_offer,
        F.text,
        OfferNews.typing_text,
    )
    router.message.register(
        cmd_news_offer,
        F.text,
        OfferNews.typing_contact,
    )
    router.message.register(
        cmd_news_input_error,
        OfferNews.typing_text,
    )
    router.message.register(
        cmd_news_input_error,
        OfferNews.typing_contact,
    )

    # Отправить новость
    router.callback_query.register(call_news_offer_send, F.data == "news_offer_send")

    # Отменить отправку новости
    router.callback_query.register(call_news_offer_cancel, F.data == "news_offer_cancel")
    
    logger.success("Роутер для ЛС готов.")

    return router

