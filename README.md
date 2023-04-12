# Чат на django

Этот проект создавался для выполнения домашней работы по RPM.
Инструкция написана для пользователей Ubunta Linux.

## Установка проекта

- `sudo apt-get update`

### Если у вас есть docker поднимите контейнер, например я использую postgresql

- `docker run --name mycontainer -p 5432:5432 -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydb -d postgres`

- `git clone https://github.com/vylkov/rpm-hws_7-1_2023.git`

### Перед установкой зависимостей рекомендуем создать виртуальную среду и активировать её

- `python3 -m venv venv`

- `source venv/bin/activate`

### Установите зависимости

- `pip install -r requirements.txt`

### Настройте файл settings.py в rpmchat

Обязательно настройте database
Например для созданой бд в докере будет выглядеть так

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',                      
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

## Запуск проекта

1. Перейдите в папку rpmchat.

2. Создайте и примените миграции: `python manage.py makemigrations` и `python manage.py migrate`

3. Запустите сервер: `python manage.py runserver`

# Наслаждайтесь.