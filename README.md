
# Kino Keeper

Kino Keeper - это приложение для управления избранными фильмами с использованием [Kinopoisk API Unofficial](https://kinopoiskapiunofficial.tech/). Оно позволяет пользователям искать фильмы, просматривать детали и добавлять их в избранное.

## Оглавление

- [Функциональные возможности](#функциональные-возможности)
- [Установка](#установка)
- [Использование](#использование)
- [Зависимости](#зависимости)
- [Лицензия](#лицензия)

## Функциональные возможности

- **Поиск фильмов:** Пользователи могут искать фильмы по ключевым словам и получать результаты, включая название, год, описание и рейтинг.
- **Просмотр деталей фильма:** Каждый фильм можно просмотреть в деталях, включая информацию о жанрах, стране, времени показа и постере.
- **Избранные фильмы:** Пользователи могут добавлять фильмы в избранное, что позволяет им легко находить и отслеживать свои любимые фильмы.
- **Управление избранными фильмами:** Пользователи могут удалять фильмы из избранного и просматривать весь список своих избранных фильмов.
- **Аутентификация и авторизация:** Пользователи могут просматривать и управлять только своими избранными фильмами.

## Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/DevGruz/kino-keeper.git
cd kino-keeper
```

### 2. Настройка окружения

Создайте файл .env в корне проекта и настройте необходимые переменные окружения:. В корне проекта есть пример .env файла с названием .env-example
```
PROJECT_NAME=KinoKeeper
SECRET_KEY=your_secret_key

KINOPOISK_UNOFFICIAL_URL=https://kinopoiskapiunofficial.tech
KINOPOISK_UNOFFICIAL_API_KEY=

POSTGRES_HOST=kino-keeper-db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=kino-keeper
```

### 3. Запуск с Docker

В проекте есть docker-compose.yml файл для быстрой настройки и запуска
```bash
docker-compose up --build
```

## Использование
После запуска приложения вы можете получить доступ к API по адресу http://localhost:8000
### Эндпоинты
- **POST /register** - Регистрация нового пользователя.
- **POST /login** - Аутентификация пользователя.
- **POST /logout** - Выход пользователя.

- **GET /profile** - Получение текущего пользователя.

- **GET /movies/search** - Поиск фильмов по ключевому слову.
- **GET /movies/{kinopoisk_id}** - Получение деталей фильма.
- **GET /movies/favorites** - Получение списка избранных фильмов.
- **POST /movies/favorites** - Добавление фильма в избранное.
- **DELETE /movies/favorites/{kinopoisk_id}** - Удаление фильма из избранного.


### Доступ к Swagger-документации
Для удобства разработки и тестирования API доступна Swagger-документация. Перейдите по адресу http://127.0.0.1:8000/docs, чтобы просмотреть и протестировать все доступные эндпоинты.

## Зависимости
Проект использует следующие ключевые библиотеки:

-  **FastAPI**: Фреймворк для разработки веб-приложений.
-  **SQLAlchemy**: ORM для работы с базами данных.
-  **Pydantic**: Для валидации данных.
-  **FastAPI Users**: Библиотека для добавления системы регистрации и аутентификации.
-  **httpx**: Для выполнения асинхронных HTTP-запросов.

## Лицензия
Этот проект лицензирован под MIT License - подробности см. в файле [LICENSE](https://github.com/DevGruz/kino-keeper/blob/main/LICENSE).