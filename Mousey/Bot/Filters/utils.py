from aiogram import Router
from aiogram.filters import BaseFilter


def add_filters(router: Router, update_type: str, *filters: BaseFilter) -> None:
    """
        Добавить фильтр на указанных тип обновлений к перечисленным роутерам.

        update_type: str = "message", "callback" или "all".
    """
    for filter in filters:
        if update_type in ("message", "all"):
            router.message.filter(filter)
            
        if update_type in ("callback", "all"):
            router.callback_query.filter(filter)

