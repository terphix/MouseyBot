import json

from aiogram import Bot
from aiogram.types.bot_command import BotCommand
from aiogram.types.bot_command_scope_all_private_chats import BotCommandScopeAllPrivateChats

from loguru import logger

from Mousey.Misc import BOT_SETTINGS_DIR


async def set_profile_info(bot: Bot) -> None:
    """
        Установка всей информации в профиле для бота.
        Имя, описание, аватар...
    """
    with open(BOT_SETTINGS_DIR / "settings.json", "r", encoding="utf-8") as file:
        bot_info = json.load(file)

    await bot.set_my_name(bot_info["name"])
    await bot.set_my_short_description(bot_info["about"])
    await bot.set_my_description(bot_info["description"])

    logger.info("Данные в профиле бота обновлены.")


async def set_command_menu(bot: Bot) -> None:
    """
        Установка меню пользовательских команд в Telegram для бота.
    """
    with open(BOT_SETTINGS_DIR / "settings.json", "r", encoding="utf-8") as file:
        bot_info = json.load(file)

    await bot.set_my_commands(
        [
            BotCommand(command=command_info["name"], description=command_info["description"])
            for command_info in bot_info["commands"]
        ],
        scope=BotCommandScopeAllPrivateChats(),
    )

    logger.info("Меню команд для бота настроено.")


