from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.filters.command import CommandObject

from Mousey.Misc import UserRole
from Mousey.Database import update_user_role


async def cmd_sticker_id(message: Message):
    """
        Отправка ID стикера.
    """
    await message.answer(
        text=str(message.sticker.file_id),
    )


async def cmd_update_role(
        message: Message,
        command: CommandObject,
        session: AsyncSession,
    ) -> None:
    """
        Обновление роли по ID.
    """
    args = command.args if command.args is None else command.args.split()
    roles = [role.value for role in UserRole]

    if args is None or not (len(args) == 2 and args[0] in roles and args[1].isdigit()):
        await message.answer(
            text=_("Обновление роли, необходимо ввести существующую роль").format(roles=roles),
        )
        return
    
    await update_user_role(session, int(args[1]), args[0])

    await message.answer(
        text=_("Обновление роли, роль успешно обновлена"),
    )

