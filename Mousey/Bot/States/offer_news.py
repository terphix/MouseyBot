from aiogram.fsm.state import StatesGroup, State


class OfferNews(StatesGroup):
    typing_text = State()
    typing_contact = State()

