from os import getenv

from loguru import logger

from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook
from aiogram.fsm.storage.redis import RedisStorage

from .settings import set_command_menu, set_profile_info

from .Handlers import setup_routers
from .Middlewares import i18n_middleware, DatabaseSessionMiddleware

from Mousey.Redis import redis
from Mousey.Database import create_db, drop_db, session_maker


@logger.catch
async def start(
        to_drop_db: bool,
        to_update_telegram_profile: bool,
    ) -> None:
    """
        Запуск бота
    """
    # Загрузка базы данных
    if to_drop_db:
        await drop_db()
        logger.warning("База данных очищена.")
     
    await create_db()

    # Настройка бота
    bot = Bot(token=getenv("BOT_TOKEN"))
    await set_command_menu(bot=bot)
    
    # Обновление профиля
    if to_update_telegram_profile:
        await set_profile_info(bot=bot)

    # Настройка диспетчера
    dp = Dispatcher(
        storage=RedisStorage(redis=redis),
    )
    
    # Добавление мидлвари для диспетчера
    dp.message.middleware(i18n_middleware)
    dp.callback_query.middleware(i18n_middleware)

    dp.update.middleware(DatabaseSessionMiddleware(session_pool=session_maker))
    
    logger.success("Все мидлвари успешно добавлены.")

    # Добавление роутеров для диспетчера
    setup_routers(dispatcher=dp)
    logger.success("Все роутеры успешно добавлены.")
    
    # Старт пуллинга бота
    await bot(DeleteWebhook(drop_pending_updates=True))
    logger.debug("Все Telegram запросы для бота удалены.")

    logger.success("Старт пуллинга бота.")
    await dp.start_polling(bot)

