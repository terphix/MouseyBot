import os

from dotenv import load_dotenv
from loguru import logger
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from Mousey.Misc import CONFIG_FILE_PATH

from .Models import Base
from .utils import add_main_admin

load_dotenv(CONFIG_FILE_PATH)
engine = create_async_engine(url=os.getenv("DB_URL"), echo=True)
session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


@logger.catch
async def create_db():
    """
    Загрузка или создание новой базы данных.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.debug("База данных загружена.")

    async with session_maker() as session:
        await add_main_admin(session)


@logger.catch
async def drop_db():
    """
    Полная очистка базы данных.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    logger.warning("База данных очищена.")
