import sys
import asyncio

from loguru import logger
from dotenv import load_dotenv

from .Bot import start
from .Misc import CONFIG_FILE_PATH, LOG_DIR


def main():
    # Инициализация логера
    logger.add(
        LOG_DIR / "{time:YYYY-MM-DD__HH:mm!UTC}.log",
        format="{time:HH:mm::ss!UTC} |  {level}  |  {file}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="3 days",
        compression="zip",
    )
    logger.info("Время для журнала отладки: HH:mm:ss")
    logger.info("Часовой пояс: UTC")

    logger.info("Удачи!")
    load_dotenv(CONFIG_FILE_PATH)
    logger.info("Переменные окружения из файла конфигурации загружены.")

    # Запуск бота
    logger.debug("Пытаюсь запустить бота...")
    asyncio.run(
        start(
            to_drop_db="drop_db" in sys.argv,
            to_update_telegram_profile="update_telegram_profile" in sys.argv,
        )
    )


if __name__ == "__main__":
    try:
        main()
        logger.debug("Бот остановлен.")
    except Exception as error:
        logger.warning(f"Неизвестная ошибка: {error}")
