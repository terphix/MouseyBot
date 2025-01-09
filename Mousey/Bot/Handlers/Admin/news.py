from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession

from Mousey.Misc import UserRole
from Mousey.Database import (
    get_news,
    see_news,
    check_user,
    update_user_role,
    get_next_unseen_news,
    get_prev_unseen_news,
)
from Mousey.Bot.Keyboards import (
    get_back_markup,
    get_admin_news_markup,
    get_admin_news_offer_markup,
)


#######################
### Вспомогательное ###
#######################
def __get_offer_text(news) -> str:
    # Стандартная информация для новости
    if news is not None:
        telegram_id = news.tg_id
        telegram_username = news.tg_username or _("Админ меню новости, профиль скрыт")
        text = news.text[:512] + "..." if len(news.text) >= 512 else ""

        # Опциональное получение контактов
        contact = news.contact

        if contact is not None:
            contact = contact[:256]
            contact += "..." if len(contact) >= 256 else ""
        else:
            contact = _("Админ меню новости, контакт не указан")

    return _("Админ меню новости, информация о новости").format(
            telegram_id=telegram_id,
            telegram_username=telegram_username,
            text=text,
            contact=contact,
        ) if news is not None else _("Админ меню новости непрочитанных нет")


##############
### Вызовы ###
##############
async def call_news_menu(call: CallbackQuery) -> None:
    """
        Админ-меню для просмотра предложенных новостей.
    """
    await call.message.edit_text(
        text=_("Админ меню новости"),
        reply_markup=get_admin_news_markup(),
    )


async def call_news_favorite(call: CallbackQuery, session: AsyncSession) -> None:
    """
        Избранные новости для редактирования и использования.
    """
    await call.message.edit_text(
        text=_("Функция в разработке"),
        reply_markup=get_back_markup("Назад", "admin_news_menu")
    )


async def call_news_offer_menu(call: CallbackQuery, session: AsyncSession):
    """
        Меню для работы с предложенными новостями через Callback'и.
    """
    data = call.data.split("_")
    news_id = int(data[3])

    # Специфичные требования для первой новости
    if news_id == 0:
        news = await get_next_unseen_news(session, news_id)

        await call.message.edit_text(
            text=__get_offer_text(news),
            reply_markup=get_back_markup(callback_data="admin_news_menu") if news is None \
                else get_admin_news_offer_markup(news)
        )
        return

    # Обработка callback'а с действием
    step = data[4]
    
    # Выбрана распечатка новости
    if step == "print":
        news = await get_news(session, news_id)
        await call.message.answer(text=call.message.text)
        await call.message.answer(text=news.text)
        await call.message.answer(
            text=news.contact or _("Админ меню новости, контакт не указан")
        )
        return

    # Выбран просмотр новости
    if step == "seen":
        await see_news(session, news_id)

        await call.answer(
            text=_("Новость просмотрена"),
            show_alert=False,
        )
        return

    # Выбран бан автора новости
    if step == "ban":
        news = await get_news(session, news_id)
        user = await check_user(session, news.tg_id)

        reasons = {
            UserRole.USER.value: _("Админ новости, автор новости забанен"),
            UserRole.BANNED.value: _("Админ новости, автор новости уже был забанен"),
        }

        if reasons.get(user.role) is not None:
            await see_news(session, news_id)
            await update_user_role(session, user.tg_id, UserRole.BANNED)

        await call.answer(
            text=reasons.get(user.role, _("Админ новости, нельзя забанить администратора")),
            show_alert=True,
        )
        return

    # Выбрана следующая или предыдущая новость
    news = await get_next_unseen_news(session, news_id) if step == "next" else \
        await get_prev_unseen_news(session, news_id)

    await call.message.edit_text(
        text=__get_offer_text(news),
        reply_markup=get_admin_news_offer_markup(news=news)
    )

