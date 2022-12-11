![yamdb_final workflow](https://github.com/px2005/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
## Проект YaMDb.
### Описание
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title). Произведения делятся на категории: "Книги", "Фильмы", "Музыка". Список категорий (Category) может быть расширен.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории "Книги" могут быть произведения "Винни Пух и все-все-все" и "Марсианские хроники", а в категории "Музыка" — песня "Давеча" группы "Насекомые" и вторая сюита Баха. Произведению может быть присвоен жанр из списка предустановленных (например, "Сказка", "Рок" или "Артхаус"). Новые жанры может создавать только администратор.
Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы (Review) и выставляют произведению рейтинг.

## Стек технологий

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)


# Ресурсы API YaMDb
**AUTH**: аутентификация.

**USERS**: пользователи.

**TITLES**: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).

**CATEGORIES**: категории (типы) произведений ("Фильмы", "Книги", "Музыка").

**GENRES**: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.

**REVIEWS**: отзывы на произведения. Отзыв привязан к определённому произведению.

**COMMENTS**: комментарии к отзывам. Комментарий привязан к определённому отзыву.

# Алгоритм регистрации пользователей
Пользователь отправляет POST-запрос с параметром email на `/api/v1/auth/email/`.
YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email (функция в разработке).
Пользователь отправляет POST-запрос с параметрами email и confirmation_code на `/api/v1/auth/token/`, в ответе на запрос ему приходит token (JWT-токен).
Эти операции выполняются один раз, при регистрации пользователя. В результате пользователь получает токен и может работать с API, отправляя этот токен с каждым запросом.

# Пользовательские роли
**Аноним** — может просматривать описания произведений, читать отзывы и комментарии.

**Аутентифицированный пользователь (user)** — может читать всё, как и Аноним, дополнительно может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы и ставить им оценки; может редактировать и удалять свои отзывы и комментарии.

**Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя плюс право удалять и редактировать любые отзывы и комментарии.

**Администратор (admin)** — полные права на управление проектом и всем его содержимым. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

**Администратор Django** — те же права, что и у роли Администратор.

### Как запустить проект:
Подготовка сервера для запуска проекта:
Создайте и активируйте виртуальное окружение, обновите pip:
python3 -m venv venv
. venv/bin/activate
python3 -m pip install --upgrade pip
Отредактируйте файл nginx/default.conf и в строке server_name впишите IP виртуальной машины (сервера).
Скопируйте подготовленные файлы docker-compose.yaml и nginx/default.conf из вашего проекта на сервер:
scp docker-compose.yaml <username>@<host>/home/<username>/docker-compose.yaml
sudo mkdir nginx
scp default.conf <username>@<host>/home/<username>/nginx/default.conf
В репозитории на Гитхабе добавьте данные в Settings - Secrets - Actions secrets:
DOCKER_USERNAME - имя пользователя в DockerHub
DOCKER_PASSWORD - пароль пользователя в DockerHub
HOST - ip-адрес сервера
USER - пользователь
SSH_KEY - приватный ssh-ключ (публичный должен быть на сервере)
PASSPHRASE - кодовая фраза для ssh-ключа
DB_ENGINE - django.db.backends.postgresql
DB_HOST - db
DB_PORT - 5432
SECRET_KEY - секретный ключ приложения django (необходимо чтобы были экранированы или отсутствовали скобки)
ALLOWED_HOSTS - список разрешённых адресов
TELEGRAM_TO - id своего телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
TELEGRAM_TOKEN - токен бота (получить токен можно у @BotFather, /token, имя бота)
DB_NAME - postgres (по умолчанию)
POSTGRES_USER - postgres (по умолчанию)
POSTGRES_PASSWORD - postgres (по умолчанию)
Как запустить проект на сервере:
Установите Docker и Docker-compose:
sudo apt install docker.io
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
Проверьте корректность установки Docker-compose:
sudo  docker-compose --version
Создайте папку nginx:
mkdir nginx

##После успешного деплоя:

Соберите статические файлы (статику):

```docker-compose exec web python manage.py collectstatic --no-input```

Примените миграции:

```docker-compose exec web python manage.py makemigrations```

```docker-compose exec web python manage.py migrate --noinput```

Создайте суперпользователя:

```docker-compose exec web python manage.py createsuperuser```

Ссылки проекта:

http://62.84.122.171/api/v1/ http://62.84.122.171/admin/ http://62.84.122.171/redoc/

### Авторы
Александр Горыничев
