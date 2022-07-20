![yamdb_final workflow](https://github.com/px2005/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
## Проект YaMDb.
### Описание
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.

Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

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
После успешного деплоя:
Соберите статические файлы (статику):

docker-compose exec web python manage.py collectstatic --no-input
Примените миграции:

docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate --noinput
Создайте суперпользователя:

docker-compose exec web python manage.py createsuperuser

или

docker-compose exec web python manage.py loaddata fixtures.json

Ссылки проекта:

http://62.84.122.171/api/v1/ http://62.84.122.171/admin/ http://62.84.122.171/redoc/
