from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class ChatTypeFilter(BaseFilter):
    """
        Фильтрация обновлений в зависимости от чата.
    """
    def __init__(self, chat_type: Union[str, list]) -> None:
        self.chat_type = chat_type

    async def __call__(self, update: Union[Message, CallbackQuery]) -> bool:
        if isinstance(update, Message):
            chat_type = update.chat.type
        elif isinstance(update, CallbackQuery):
            chat_type = update.message.chat.type

        if isinstance(self.chat_type, str):
            return chat_type == self.chat_type
        else:
            return chat_type in self.chat_type

