## Проект Foodgram

> Kittygram — это сервис для хранения информации о котиках.
> Цель этого сайта — дать возможность пользователям создавать и хранить рецепты на онлайн-платформе. Кроме того, можно скачать список продуктов, необходимых для приготовления блюда, просмотреть рецепты друзей и добавить любимые рецепты в список избранных.
> Чтобы использовать все возможности сайта — нужна регистрация. Проверка адреса электронной почты не осуществляется, вы можете ввести любой email.
> Заходите и делитесь своими любимыми рецептами!

## Адрес сайта https://hostfoodgram.ddns.net

## Стек использованных технологий:
* Django==3.2
* djangorestframework==3.12.4
* Python==3.9.13
* djoser==2.1.0
* postgresql==13.10
* gunicorn==20.1.0
* Nginx
* Docker Compose
* GitHub Actions

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/KatarinaStred/foodgram.git
```

```
cd foodgram
```

Через CI/CD:

1. Настраиваем секретные данные в настройках репозитория:
Перейдите в настройки репозитория — Settings, выберите на панели слева Secrets and Variables → Actions, нажмите New repository secret и добавляйте переменные:
* DOCKER_PASSWORD - пароль от Docker Hub
* DOCKER_USERNAME - имя пользователя Docker Hub
* HOST - ip сервера
* USER - имя пользователя сервера
* SSH_KEY - ключ ssh для доступа к удаленному серверу
* SSH_PASSPHRASE - пароль ssh
* TELEGRAM_TO - id пользователя TELEGRAM
* TELEGRAM_TOKEN - TELEGRAM токен для отправки сообщений

2. Создайте файл .env в корне проекта и добавьте необходимые переменные:
* POSTGRES_DB=db_name
* POSTGRES_USER=user_name
* POSTGRES_PASSWORD=password
* DB_NAME=db_name
* DB_HOST=db
* DB_PORT=5432
* ALLOWED_HOST = ваш_ip
* ALLOWED_HOST_DOMAIN = ваше_имя_домена(если есть)
* DEBUG = False

При каждом пуше в ветку main GitHub Actions автоматически запустит тесты, соберет Docker-образы, и развернёт проект на сервере.
После успешного выполнения, образы будут опубликованы на DockerHub, а в Telegram будут отправлено сообщение "Деплой успешно выполнен!"


## Всю документацию можно посмотреть по адресу https://hostfoodgram.ddns.net/api/docs/

Автор: Екатерина Михайлова