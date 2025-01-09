from aiogram.utils.i18n import gettext as _
from aiogram.types import Message, CallbackQuery

from Mousey.Bot.Keyboards import get_admin_menu_markup, get_back_markup


#################
### Сообщения ###
#################
async def cmd_admin_menu(message: Message) -> None:
    """
        Вызов меню для администрации командой.
    """
    await message.answer(
        text=_("Админ меню"),
        reply_markup=get_admin_menu_markup(),
    )


#############
### Вызовы ###
#############
async def call_admin_menu(call: CallbackQuery) -> None:
    """
        Вызов меню для администрации с помощью Callback'а.
    """
    await call.message.edit_text(
        text=_("Админ меню"),
        reply_markup=get_admin_menu_markup(),
    )


async def call_admin_commands(call: CallbackQuery) -> None:
    """
        Просмотр команд для администратора.
    """
    await call.message.edit_text(
        text=_("Список админ команд"),
        reply_markup=get_back_markup(callback_data="admin_menu"),
    )

