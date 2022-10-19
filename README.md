# REST API сервиса YaMDb

### Описание
Проект представляет собой API для проекта YaMDb  — базы отзывов о фильмах, книгах и музыке.
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». 
В каждой категории есть произведения: книги, фильмы или музыка. 
Произведению может быть присвоен жанр (Genre) из списка предустановленных. Новые жанры может создавать только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число), затем из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

### Технологии 
- Python
- Django
- Django REST Framework
- SQLlite
- Simple-JWT

### Особенности
- Применены вьюсеты
- Для аутентификации использованы JWT-токены
- У неаутентифицированных пользователей доступ к API только на чтение
- Аутентифицированным пользователям разрешено изменение и удаление своего контента; в остальных случаях доступ предоставляется только для чтения

### Установка
- Склонировать репозиторий

```commandline
git clone github.com/podlev/api_yamdb.git
```

- Создать и активировать виртуальное окружение для проекта

```commandline
python -m venv venv

source venv/scripts/activate (Windows)    
source venv/bin/activate (MacOS/Linux)

python3 -m pip install --upgrade pip
```

- Установить зависимости

```commandline
python pip install -r requirements.txt
```

- Сделать миграции

```commandline
python manage.py makemigrations
python manage.py migrate
```

- Запустить сервер

```commandline
python manage.py runserver
```

### Примеры

- Для доступа к API необходимо получить токен: POST-запрос localhost:8000/api/v1/auth/signup/ передав поля username и email. API отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
```
{ 
    "email": "string",
    "username": "string" 
}
```

- Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/,в ответе на запрос ему приходит token (JWT-токен).
```
{ 
    "username": "string",
    "confirmation_code": "string" 
}
```

- После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт /api/v1/users/me/ и заполнить поля в своём профайле.

- Затем, отправляя токен с каждым запросом, можно будет обращаться к методам, например: 
```
/api/v1/titles/ (GET, POST, PATCH, DELETE)    
/api/v1/genre/ (GET, POST, DELETE)    
/api/v1/categories/ (GET, POST, DELETE)    
```
- При отправке запроса необходимо передать токен в заголовке Authorization: Bearer <токен>
- Основной список ресурсов API /api/v1/
### Авторы
[Лев Подъельников](https://github.com/podlev) (users, permissions) | [Виталий Сергеев](https://github.com/Vitaly1996) (API) | [Ксения Зверева](https://github.com/Ksenia175) (Reviews)
