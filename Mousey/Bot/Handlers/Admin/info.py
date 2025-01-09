from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from Mousey.Database import get_database_data


async def cmd_admin_database_info(message: Message, session: AsyncSession) -> None:
    """
        Получить всю важную информацию из БД.
    """
    data = await get_database_data(session)

    await message.answer(
        text=_("Админ пинг базы данных").format(
            users_count=data["users_count"],
            news_count=data["news_count"],
        ),
    )

