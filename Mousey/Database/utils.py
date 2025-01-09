"""
    Файл с кастомными функциями для обращения к базе данных.
"""
from os import getenv
from typing import Tuple

from loguru import logger

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func

from .Models import Users, News

from Mousey.Misc import UserRole, NewsStatus


"""
    Изменение состояния пользователя в базе данных.
"""
async def _get_user(session: AsyncSession, telegram_id: int) -> Users | None:
    """
        Получить пользователя из БД.
        Возвращает либо объект пользователя, либо None, если пользователя нет.
    """
    query = select(Users).where(Users.tg_id == telegram_id)
    result = await session.execute(query)

    return result.scalar()


async def _add_user(session: AsyncSession, telegram_id: int) -> Users:
    """
        Добавить пользователя в БД.
        Возвращает только что добавленный объект пользователя.
    """
    user = Users(tg_id=telegram_id)
    session.add(user)

    await session.commit()

    return user


async def check_user(session: AsyncSession, telegram_id: int) -> Users:
    """
        Проверяет, есть ли пользователь в БД.
        Если его нет, то добавляет.
        Всегда возвращает объект пользователя.
    """
    result = await _get_user(session, telegram_id)

    if result is not None:
        return result

    return await _add_user(session, telegram_id)


async def get_news_statistics(session: AsyncSession, telegram_id: int) -> Tuple[int]:
    """
        Получить количество всех предложенных пользователем новостей
        и тех, которые не просмотрели.
    """
    user = await check_user(session, telegram_id)

    return user.all_news, user.unseen_news


async def update_user_role(session: AsyncSession, telegram_id: int, role: UserRole) -> None:
    """
        Обновление роли пользователя.
        Ничего не возвращает.
    """
    user = await check_user(session, telegram_id)

    if isinstance(role, UserRole):
        role = role.value

    query = update(Users).where(Users.tg_id == user.tg_id).values(
        role=role
    ) 

    await session.execute(query)

    await session.commit()


async def add_main_admin(session: AsyncSession) -> None:
    """
        Добавить главного администратора в БД.
    """
    main_admin_id = getenv("MAIN_ADMIN_ID")

    if not main_admin_id.isdigit():
        logger.warning("Основной главный администратор не указан!")
        return
    
    main_admin_id = int(main_admin_id)
    
    await check_user(session, main_admin_id)
    await update_user_role(session, main_admin_id, UserRole.MAIN_ADMIN)
    
    logger.info("Основной главный администратор добавлен в базу данных.")


"""
    Взаимодействие с БД для новостей.
"""
async def _change_news_count(
        session: AsyncSession,
        telegram_id: int,
        add_count_all: int,
        add_count_unseen: int
    ) -> None:
    """
        Изменения количества новостей для пользователя.
    """
    user = await check_user(session, telegram_id)

    query = update(Users).where(Users.tg_id == user.tg_id).values(
        all_news=user.all_news + add_count_all,
        unseen_news=user.unseen_news + add_count_unseen,
    )

    await session.execute(query)

    await session.commit()


async def add_news(
        session: AsyncSession,
        telegram_id: int,
        telegram_username: str,
        text: str,
        contact: str | None
    ) -> None:
    """
        Добавление новости в БД.
    """
    news = News(
        tg_id=telegram_id,
        tg_username=telegram_username,
        text=text,
        contact=contact,
    )
    session.add(news)
    
    await _change_news_count(
        session=session,
        telegram_id=telegram_id,
        add_count_all=1,
        add_count_unseen=1,
    )

    await session.commit()


async def get_next_unseen_news(session: AsyncSession, news_id: int) -> News | None:
    """
        Получить следующую по счету непрочитанную новость.
    """
    query = select(News)\
            .where(News.status == NewsStatus.UNSEEN.value, News.news_id > news_id)\
            .order_by(News.news_id.asc())\
            .limit(1)
    
    result = await session.execute(query)
    
    return result.scalar()


async def get_prev_unseen_news(session: AsyncSession, news_id: int) -> News | None:
    """
        Получить предыдущую по счету непрочитанную новость.
    """
    query = select(News)\
            .where(News.status == NewsStatus.UNSEEN.value, News.news_id < news_id)\
            .order_by(News.news_id.desc())\
            .limit(1)
    
    result = await session.execute(query)
    
    return result.scalar()


async def get_news(session: AsyncSession, news_id: int) -> News | None:
    """
        Вспомогательная функция для получения новости из БД по ключу.
    """
    query = select(News).where(News.news_id == news_id)
    result = await session.execute(query)

    return result.scalar()


async def see_news(session: AsyncSession, news_id: int) -> bool:
    """
        Удалить просмотренную новость.
    """
    news = await get_news(session, news_id)

    if news is None:
        return False
    
    query = delete(News).where(News.news_id == news.news_id)
    await session.execute(query)
    await session.commit()
    
    user = await check_user(session, news.tg_id)
    await _change_news_count(
        session=session,
        telegram_id=user.tg_id,
        add_count_all=0,
        add_count_unseen=-1,
    )

    return True


"""
    Сбор данных из БД.
"""
async def get_database_data(session: AsyncSession) -> dict:
    """
        Сбор полезной информации и данных от БД.
    """
    data = dict()
    data["users_count"] = (
        await session.execute(
            select(func.count()).select_from(Users)
        )
    ).scalar()

    data["news_count"] = (
        await session.execute(
            select(func.count()).select_from(News)
        )
    ).scalar()

    return data

