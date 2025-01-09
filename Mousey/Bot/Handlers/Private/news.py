from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import CallbackQuery, Message

from .utils import call_cancel

from Mousey.Misc import UserRole
from Mousey.Bot.States import OfferNews
from Mousey.Database import (
    add_news,
    check_user,
    get_news_statistics,
)
from Mousey.Bot.Keyboards import (
    get_back_markup,
    get_news_menu_markup,
    get_offer_news_markup,
)


#######################
### Вспомогательное ###
#######################
async def __get_news_offer_text(state: FSMContext) -> str:
    data = await state.get_data()
    
    news_text = _("Текст для новости отсутствует")
    news_contact = _("Контакты для новости отсутствуют")

    if data.get("news_text") is not None:
        news_text = _("Шаблон для вставки текста новости").format(
            text=data["news_text"][:512]
        )

    if data.get("news_contact") is not None:
        news_contact = _("Шаблон для вставки контактов новости").format(
            contact=data["news_contact"][:256]
        )

    news_text += "..." if len(news_text) >= 512 else ""
    news_contact += "..." if len(news_contact) >= 256 else ""

    return _("Шаблон для формы отправки новости").format(
        news_text=news_text,
        news_contact=news_contact,
    )


def __check_user_for_offer(data: dict, user) -> bool:
    if user.role in (UserRole.ADMIN.value, UserRole.MAIN_ADMIN.value):
        return data.get("news_text") is not None
    
    if user.role == UserRole.USER.value:
        return data.get("news_text") is not None and user.unseen_news <= 3
    
    return False


#################
### Сообщения ###
#################
async def cmd_news_offer(message: Message, state: FSMContext) -> None:
    """
        Меню, чтобы предложить новость.
    """
    current_state = await state.get_state()

    if current_state == OfferNews.typing_text:
        await state.update_data(news_text=message.text)

    elif current_state == OfferNews.typing_contact:
        await state.update_data(news_contact=message.text)

    await state.set_state()

    await message.answer(
        text=await __get_news_offer_text(state),
        reply_markup=get_offer_news_markup(),
    )


async def cmd_news_input_error(message: Message, state: FSMContext) -> None:
    """
        Некоректная отправка сообщения для предложки.
    """
    await message.answer(
        text=_("Неправильная форма данных для новости"),
    )


##############
### Вызовы ###
##############
async def call_news_menu(call: CallbackQuery) -> None:
    """
        Вызов новостного меню.
    """
    await call.message.edit_text(
        text=_("Новостное меню"),
        reply_markup=get_news_menu_markup(),
    )


async def call_news_statistics(call: CallbackQuery, session: AsyncSession) -> None:
    """
        Статистика новостей пользователя.
    """
    news_statistics = await get_news_statistics(session, int(call.from_user.id))

    await call.message.edit_text(
        text=_("Шаблон для статистики новостей").format(
            all_news=news_statistics[0],
            unseen_news=news_statistics[1],
        ),
        reply_markup=get_back_markup(callback_data="news_menu"),
    )


async def call_news_offer(call: CallbackQuery, state: FSMContext) -> None:
    """
        Меню, чтобы предложить новость.
    """
    await state.set_state()

    await call.message.edit_text(
        text=await __get_news_offer_text(state),
        reply_markup=get_offer_news_markup(),
    )


async def call_input_news_text(call: CallbackQuery, state: FSMContext) -> None:
    """
        Сообщение для ввода текста для новости.
    """
    await state.set_state(OfferNews.typing_text)
    
    await call.message.edit_text(
        text=_("Ввести текст для новости"),
        reply_markup=get_back_markup(
            button_name="Отменить отправку",
            callback_data="news_offer_cancel",
        ),
    )


async def call_input_news_contact(call: CallbackQuery, state: FSMContext) -> None:
    """
        Сообщение для ввода контактов для новости.
    """
    await state.set_state(OfferNews.typing_contact)

    await call.message.edit_text(
        text=_("Ввести контакты для новости"),
        reply_markup=get_back_markup(
            button_name="Отменить отправку",
            callback_data="news_offer_cancel",
        ),
    )


async def call_news_offer_cancel(call: CallbackQuery, state: FSMContext):
    await call_cancel(call, state, callback_data="news_menu")


async def call_news_offer_send(
        call: CallbackQuery,
        state: FSMContext,
        session: AsyncSession,
    ) -> None:
    """
        Сообщение об отправке новости.
    """
    data = await state.get_data()
    user = await check_user(session, call.from_user.id)

    if __check_user_for_offer(data, user):
        await add_news(
            session=session,
            telegram_id=call.from_user.id,
            telegram_username=call.from_user.username,
            text=data["news_text"],
            contact=data.get("news_contact"),
       )
        await call.message.edit_text(
            text=_("Новость успешно отправлена"),
            reply_markup=get_back_markup(callback_data="news_menu"),
        )
        await state.clear()
        return
    
    reasons = {
        "text": _("Отсутствует текст для новости"),
        "banned": _("Вы забанены"),
        "limite": _("Превышен лимит непрочитанных новостей"),
    }
    
    if data.get("news_text") is None:
        reason = reasons["text"]

    elif user.role == UserRole.BANNED.value:
        reason = reasons["banned"]

    else:
        reason = reasons["limite"]

    await call.message.edit_text(
        text=_("Шаблон новость не отправлена").format(reason=reason),
        reply_markup=get_back_markup(callback_data="news_menu"),
    )
    await state.clear()

