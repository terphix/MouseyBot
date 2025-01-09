from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from Mousey.Misc import UserRole
from Mousey.Database import check_user


class UserRoleFilter(BaseFilter):
    '''
        Фильтрация сообщений на основе их роли в БД.
    '''
    def __init__(self, user_role: Union[UserRole, list]) -> None:
        if isinstance(user_role, list):
            self.user_role = [ role.value for role in user_role ]
        else:
            self.user_role = [ user_role.value ]

    async def __call__(self, update: Union[Message, CallbackQuery], session) -> bool:
        if isinstance(update, Message):
            telegram_id = update.from_user.id
        elif isinstance(update, CallbackQuery):
            telegram_id = update.from_user.id
        
        user = await check_user(session, telegram_id)
        
        return user.role in self.user_role

