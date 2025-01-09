from aiogram.utils.i18n import I18n
from aiogram.utils.i18n.middleware import ConstI18nMiddleware

from Mousey.Misc import LOCALE_DIR


# Создание мидлвари для локализация бота.
i18n = I18n(path=LOCALE_DIR, default_locale="ru", domain="bot")
i18n_middleware = ConstI18nMiddleware(i18n=i18n, locale="ru")

