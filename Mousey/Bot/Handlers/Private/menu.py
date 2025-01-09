from aiogram.utils.i18n import gettext as _
from aiogram.types import Message, CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession

from Mousey.Database import check_user
from Mousey.Bot.Keyboards import get_menu_markup, get_back_markup


#################
### Сообщения ###
#################
async def cmd_menu(message: Message, session: AsyncSession) -> None:
    """
        Отправка главного меню бота сообщением.
    """
    await check_user(
        session=session,
        telegram_id=message.from_user.id,
    )

    await message.answer(
        text=_("Полное главное меню"),
        reply_markup=get_menu_markup(),
    )


#######################
### Обратные вызовы ###
#######################
async def call_menu(call: CallbackQuery, session: AsyncSession) -> None:
    """
        Вызов главного меню с помощью колбека.
    """
    await check_user(
        session=session,
        telegram_id=call.from_user.id,
    )

    await call.message.edit_text(
        text=_("Краткое главное меню"),
        reply_markup=get_menu_markup(),
    )


async def call_useful_info(call: CallbackQuery):
    """
        Полезные ссылки и прочая информация в главном меню.
    """
    user_id = call.from_user.id

    await call.message.edit_text(
        text=_("Полезная информация").format(user_id=user_id),
        reply_markup=get_back_markup(),
    )


async def call_about_bot_info(call: CallbackQuery):
    """
        Информация о боте в главном меню.
    """
    await call.message.edit_text(
        text=_("Информация о боте"),
        reply_markup=get_back_markup(),
    )

