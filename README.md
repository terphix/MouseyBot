# Мышонок Бот
 Школьный бот для Telegram, который позволяет ученикам отправлять новости в школьную группу, учавствовать в различных мероприятиях.


## Техническая часть
 - Бот написан на Python с применением асинхронной библиотеки Aiogram (States, Middlewares, Custom Filters)
 - БД - PostgreSQL, взаимодействие осуществляется с помощью библиотеки SQLAlchemy
 - Также используется асинхронный клиент Redis
 - Весь текст для диалогов бота находится в отдельном файле локализации (PyBabel)
 - Логирование главный событий + настройки для логов (автоудаление логов, сжатие файлов логов)
 - Бот полностью развертывается с помощью Docker-compose


## Содержание .env-файла
- Файл находится в корневой папке проекта.
- Вместо значений в скобках необходимо указать свои.
 1. BOT_TOKEN = (ваш токен бота)
 2. REDIS_HOST = "redis"
 3. REDIS_PORT = 6379
 4. POSTGRES_HOST = "postgres"
 5. POSTGRES_PORT = 5432
 6. POSTGRES_USER = "MouseyBot"
 7. POSTGRES_PASSWORD = (пароль для БД)
 8. POSTGRES_DB = "mousey_bot"
 9. DB_URL = "postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
 10. MAIN_ADMIN_ID = (Telegram ID главного админа)


## Как развернуть с помощью Docker (Docker-compose)
- Необходима версия Docker-compose 2.27.0 (на других может работать нестабильно)
 1. Скопируйте проект
 2. Заполните .env-файл
 3. Выполнить: docker-compose --project-directory ./ --env-file ./.env -f ./Docker/Docker-Compose.yml up

