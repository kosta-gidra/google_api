# API Google Sheets & Django

## Описание
Приложение на Django.
При помощи Celery каждые 15 секунд обращается по API к Google 
[таблице](https://docs.google.com/spreadsheets/d/1CP7mtyYyfjDkWb6sFT4G7VM-zKkiVgE_lLJ8y0mbLj4/edit#gid=0),
проверяет, что курс доллара в локальной БД за текущую дату, при необходимости запрашивает актуальный курс 
(с сайта [ЦБ](http://www.cbr.ru/development/SXML/), парсинг XML) и вносит данные с Google таблицы в локальную БД.
---

## Документация по проекту
Предварительная настройка: 
1. Создать копию Google таблицы, указанной выше. Если используется другое имя таблицы, указать его в поле _SHEET_NAME_.
2. Создать service account, сгенерировать ключ(через Manage keys) и сохранить его в формате json в корень проекта 
как _credential.json_ (смотри пример файла).
3. Открыть доступ для чтения таблицы созданному аккаунту.
4. В проекте используются переменные окружения. В рабочей дирректории необходимо создать файл .env с полями:

    ```
    PG_USER=
    PG_PASSWORD=
    ```
    При необходимости можно указать следующие поля (иначе будут использованы настройки по умолчанию):

    ```
    SECRET_KEY=
    DEBUG=
    ALLOWED_HOSTS=
    PG_PORT=
    PG_HOST=
    SHEET_NAME=
    ```
   
### Для запуска проекта необходимо выполнить команды:

```bash
pip install -r requirements.txt
docker compose up -d
python manage.py makemigrations
python manage.py migrate
celery -A google_api worker --loglevel=debug 
celery -A google_api beat 
python manage.py runserver
```
---
Доступные действия:
- Получить все заказы http://127.0.0.1:8000/orders/
- Получить текущий курс доллара http://127.0.0.1:8000/currency/

