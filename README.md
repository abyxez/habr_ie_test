# habr_ie_test

Автор проекта - Константин Мельник.

## Tecnhologies

- Python 3.11
- Django 5.0.3
- Django REST framework 3.15
- unittest
- SQLite3

### Инструкция по развёртыванию

Создать и активировать виртуальное окружение:

```text
python3 -m venv venv
```
Linux/macOS: 
```text
source venv/bin/activate
```
Windows: 
```text
source venv/Scripts/activate
```

```text
python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements:

```text
pip install -r requirements.txt
```

Запустить проект:

```text
cd /testapp
python3 manage.py makemigrations && python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

Чтобы осуществить проверку POST запроса, потребуется аутентификация:

`POST /api-token-auth/` ( eg Postman)

```json
{
    "username": "your_superuser_username", "password": "your_superuser_password"
}
```

В ответе Postman бросит token, который аутентифицирует по Authorization OAuth 2.0

____

Это простое приложение на DRF с использованием API по следующим эндпойнтам:


`POST /api/ratings/ `

Позволяет создать оценку комиксу `comic_id`, пример тела запроса:

```json
{
"comic_id": 1, "user_id": 1, "value": 4
}
```

`GET /api/comics/<int:id>/rating/`

Позволяет получить среднюю оценку пользователми комикса, если в БД присутствует хотя бы одна( по умолчанию 0):

`GET /api/comics/1/rating/`

____________

Написанные тесты вызываются из testapp/ командой

`python3 manage.py test`
