# Crypto API Demo

**Реализованный функционал:**

1. получение данных со стороннего API-сервиса
2. валидация, добавление в базу данных
3. JWT-авторизация (2 вида токенов)
4. ограничение доступа к api-маршрутам на основе роли пользователя
5. планировщик задач (ежеминутное обновление данных)

#### Что использовалось

* Python 3.12
* FastAPI
* JWT
* SQLAlchemy v2
* Alembic
* Pydantic v2
* Scheduler

#### Скриншоты

![img.png](/img%2Fimg.png)
![img.png](/img%2Fimg_1.png)
![img.png](/img%2Fimg_2.png)

#### Запуск

1. Склонируйте репозиторий
2. Активируйте виртуальное окружение
3. ```shell
    pip install -r requirements.txt
    ```
4. ```shell
    alembic upgrade heads
    ```

Для работы с API - запустите сервер:

```shell
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Демо-аккаунт API: _admin@admin.com password_

Для запуска планировщика - Вам
нужно [получить бесплатный api-ключ](https://financialmodelingprep.com/developer/docs/).   
Добавьте ключ в .env файл. Запуск планировщика:

```shell
python ./app/cron.py
```

