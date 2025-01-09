from random import choice

from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram.types import Message, CallbackQuery

from Mousey.Misc import stickers_id
from Mousey.Bot.Keyboards import get_back_markup


async def cmd_get_stickers(message: Message):
    """
        Отправка случайного школьного стикера.
    """
    await message.answer(
        text=_("Информация про набор стикеров")
    )

    await message.answer_sticker(
        sticker=choice(stickers_id),
    )


async def cmd_cancel(message: Message, state: FSMContext):
    """
        Отмена текущещей операции и очистка данных пользователя.
    """
    await state.clear()

    await message.answer(
        text=_("Отмена выполнения текущей операции"),
    )


async def call_cancel(call: CallbackQuery, state: FSMContext, callback_data: str = "menu"):
    """
        Отмена текущещей операции и очистка данных пользователя.
    """
    await state.clear()

    await call.message.edit_text(
        text=_("Отмена выполнения текущей операции"),
        reply_markup=get_back_markup(callback_data=callback_data)
    )

