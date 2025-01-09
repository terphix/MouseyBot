from typing import List

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_callback_markup(
        texts: List[str],
        data: List[str],
        *adjust: int
    ) -> InlineKeyboardMarkup:
    """
        Создание Callback-Inline клавиатуры.
        Принимает два списка: текст кнопок и данные, которые они посылают.
        Также можно указать размеры для каждой строчки клавиатуры.
        Выводит объект для reply_markup.
    """
    builder = InlineKeyboardBuilder()

    [
        builder.button(text=button[0], callback_data=button[1])
        for button in zip(texts, data)
    ]

    if len(adjust) > 0:
        builder.adjust(*adjust)
    
    return builder.as_markup()

