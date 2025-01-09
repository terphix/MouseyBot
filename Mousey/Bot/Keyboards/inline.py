from aiogram.types import InlineKeyboardMarkup

from .utils import create_callback_markup


########################
### Пользовательские ###
########################
def get_back_markup(
        button_name: str = "Назад",
        callback_data: str = "menu"
    ) -> InlineKeyboardMarkup:
    """
        Пластичная функция для отправки обратно в какое-то меню.
    """
    return create_callback_markup(
        [button_name],
        [callback_data],
    )


def get_menu_markup() -> InlineKeyboardMarkup:
    return create_callback_markup(
        ["Новости", "Полезное", "О боте"],
        ["news_menu", "useful_info", "about_bot_info"],
        1,
        2,
    )


def get_news_menu_markup() -> InlineKeyboardMarkup:
    return create_callback_markup(
       ["Предложить новость", "Статистика", "Назад"],
       ["news_offer", "news_statistics", "menu"],
       1,
       1,
       1,
    )


def get_offer_news_markup() -> InlineKeyboardMarkup:
    return create_callback_markup(
        ["Написать текст", "Указать контакты", "Отправить", "Отмена"],
        ["news_input_text", "news_input_contact", "news_offer_send", "news_offer_cancel"],
        1,
        1,
        2,
    )

#############
### Админ ###
#############
def get_admin_menu_markup() -> InlineKeyboardMarkup:
    return create_callback_markup(
        ["Новости", "Список команд"],
        ["admin_news_menu", "admin_commands"],
        1,
        1,
    )

def get_admin_news_markup() -> InlineKeyboardMarkup:
    return create_callback_markup(
        ["Предложка", "Избранные новости", "Назад"],
        ["admin_news_offer_0", "admin_news_favorite", "admin_menu"],
        1,
        1,
        1,
    )


def get_admin_news_offer_markup(news) -> InlineKeyboardMarkup:
    if news is None:
        return create_callback_markup(
            ["Начать сначала", "Выйти"],
            ["admin_news_offer_0", "admin_news_menu"],
            1,
            1,
        )

    return create_callback_markup(
        [
            "<<<",
            "Выйти",
            ">>>",
            "Просмотреть",
            "Распечатать",
            "Забанить",
        ],
        [
            f"admin_news_offer_{news.news_id}_prev",
            "admin_news_menu",
            f"admin_news_offer_{news.news_id}_next",
            f"admin_news_offer_{news.news_id}_seen",
            f"admin_news_offer_{news.news_id}_print",
            f"admin_news_offer_{news.news_id}_ban",
        ],
        3,
        1,
        1,
        1,
    )

