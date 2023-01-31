### Foodgram - Продуктовый помощник
### Описание.
Это онлайн-сервис и API для него. На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Установка локально
- Склонировать репозиторий к себе на компьютер:
```bash
git clone git@github.com:Lakrica22/foodgram-project-react.git
cd foodgram-project-react
```
- Cоздать и активировать виртуальное окружение:
```bash
python -m venv venv
```
```bash
. venv/bin/activate
```
Cоздайте файл .env в директории /infra/ с содержанием:
```bash
cd infra/
touch .env
```
```bash
SECRET_KEY=<тут ваш секртеный ключ от Django>
```

- Установите зависимости из файла requirements.txt:
```bash
cd backend/
pip install -r requirements.txt
```
- Выполните миграции:
```bash
python manage.py migrate
```
Запустите сервер:
```bash
python manage.py runserver
```
- Создайте суперпользователя:

```bash
python manage.py createsuperuser
```

- Запустите проект:

```bash
python manage.py runserver
```

### Стек технологий
Python
Django
Django REST Framework
PostgreSQL
GitHubActions

### Проект доступен по адресу:
Адрес сайта - http://51.250.64.188/

### Данные администратора:
Данные электронной почты - Admin@yandex.ru
Пароль - Admin1234
Уникальный юзернэйм - Admin
