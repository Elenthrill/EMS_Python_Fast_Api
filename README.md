# EMS Python Fast API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)

</div>

---

## 📋 О проекте

>Web сервер для CPUD операций с CIM обьектами  
пока что реализованы  регистрация и авторизация пользователей  



---

## 🏗️ Архитектура

сервер выполнен в стиле Clean Architecture и REST API  
за основу брался данный гит-репозиторий: https://github.com/BrunoTanabe/fastapi-clean-architecture-ddd-template  
(брал оттуда то, что посчитал полезным проекту)

---

## 🛠️ Стэк технологий(на текущий момент)

Python Fast Api - web фреймворк  
Dolt - база данных  
sqlalchemy - ORM  
Adminer - СУБД  
Docker-compose - для локального поднятие Dolt и Adminer  


---

## 📁 Структура проекта

```
EMS_Python_Fast_Api/
│
├── 📄 README.md                        # описание проекта, инструкции запуска
├── 📄 requirements.txt                 # зависимости(библиотеки)
├── 📄 .gitignore                       # исключения для Git
├── 📄 .env.example                     # пример переменных окружения 
│                                     
├── 📄 main.py                      # запуск приложения
│
├── 📂 core/                        # технический фундамент (не зависит от домена)
│   ├── 📄 __init__.py
│   ├── 📄 config.py                # настройки через Pydantic BaseSettings
│   ├── 📄 security.py              # хэширование паролей, JWT-токены
│   ├── 📄 database.py              # engine, async_session_factory, get_session
│   └── 📄 exceptions.py            # самописные исключения(пока пусто)
│   └── 📄 logger.py                # подключение логгов приложения(пока пусто)
│
├── 📂 domain/                      # чистые бизнес-правила (нет зависимостей от фреймворков)
│   ├── 📄 __init__.py
│   └── 📂 user/                    # описание модели user
│       ├── 📄 __init__.py
│       ├── 📄 models.py            # класс user,IUserRepository (абстрактный класс)
│
├── 📂 application/                 # определяет что делать с запросами
│   ├── 📄 __init__.py
│   └── 📂 services/                # сервисы 
│       ├── 📄 __init__.py
│       ├── 📄 auth.py              # AuthService: регистрация, вход
│       └── 📄 user.py              # UserService: получение, изменение роли
│
├── 📂 infrastructure/              # реализации под конкретные технологии (БД, очереди)
│   ├── 📄 __init__.py
│   ├── 📂 database/                # ORM-модели и, возможно, миграции
│   │   ├── 📄 __init__.py
│   │   └── 📄 models.py            # UserORM (SQLAlchemy), Base
│   └── 📂 repositories/            # конкретные реализации репозиториев
│       ├── 📄 __init__.py
│       └── 📄 user.py              # UserRepository (на основе IUserRepository, работает с Dolt)
│       # в будущем: topology.py, measurements.py
│
├── 📂 presentation/                # транспортный слой (контроллеры, middleware)
│   ├── 📄 __init__.py
│   ├── 📂 controllers/             # роутеры FastAPI
│   │   ├── 📄 __init__.py
│   │   ├── 📄 auth.py              # эндпоинты авторизации
│   │   └── 📄 user.py              # эндпоинты связанные с пользователем
│   └── 📂 middlewares/             # мидлвари(на будущее)
│       └── 📄 __init__.py
│
├── 📂 dto/                         # Data Transfer Objects (валидация запросов и ответов от сервера)
│   ├── 📄 __init__.py
│   ├── 📄 auth.py                  # схемы для запросов связанных с регистрацией/авторизацией
│   ├── 📄 user.py                  # схемы для запросов связанных с пользователем
│
├── 📂 docker/                          # Docker-конфигурация
    ├── 📄 docker-compose.yml           # поднятие Dolt и Adminer
    └── 📄 init.sql                     # скрипт инициализации БД (опционально, т.к. есть create_all)
```

---

## 📂 `/core` — Технический фундамент

> **Назначение:**  
> Содержит код, который обеспечивает жизнеспособность приложения, но не относится к предметной области. \
> - **конфигурация** (`config.py`) – параметры подключения к БД, настройки окружения;  
> - **безопасность** (`security.py`) – хеширование паролей, создание и проверка JWT-токенов;  
> - **подключение к БД** (`database.py`) – создание асинхронного движка SQLAlchemy и пулла сессий;  
> - **общие зависимости** (`dependencies.py`) – зависимости для внедрения репозиториев, сервисов и получения текущего пользователя.  
> Этот слой не знает о доменных правилах и может использоваться в любом модуле.

### 📁 `/domain` — Чистые бизнес-правила

> **Назначение:**  
> Ядро системы. Содержит сущности, перечисления, интерфейсы репозиториев и доменные сервисы, отражающие предметную область (CIM, пользователи).  
> - **models** – датаклассы (`User`, `Role`) без ORM-зависимостей;  
> - **interfaces** – абстрактные классы (`IUserRepository`), определяющие контракты для работы с хранилищем;  
> - **services** (в будущем) – чистые алгоритмы, не зависящие от инфраструктуры (расчёт режимов, проверка топологии).  
> Код здесь написан на «чистом» Python и не импортирует фреймворки или драйверы БД.

### 📁 `/application` — Сценарии использования

> **Назначение:**  
> Координирует выполнение конкретных бизнес-операций (use cases). Сервисы приложения (`AuthService`, `UserService`) принимают DTO, вызывают доменные сущности и репозитории, управляют транзакционностью и возвращают результат.  
> Слой не содержит HTTP-деталей или SQL-запросов — он зависит только от доменных интерфейсов и передаваемых DTO.

### 📁 `/infrastructure` — слой инфраструктуры(пока что только работа с бд)

> **Назначение:**  
> Техническая реализация портов, определённых в `domain`. Здесь находятся:  
> - **ORM-модели** (`database/models.py`) – SQLAlchemy-классы, соответствующие таблицам в Dolt;  
> - **реализации репозиториев** (`repositories/user.py`) – конкретная работа с базой данных: сохранение, выборка, обновление пользователей;    
> Весь код этого слоя зависит от внешних библиотек и фреймворков, но не от бизнес-логики.

### 📁 `/presentation` — Транспортный слой

> **Назначение:**  
> Прием http запросов и отправка ответов:  
> - **controllers** – FastAPI-роутеры (`auth.py`, `user.py`), принимающие запросы, валидирующие DTO и вызывающие сервисы приложения;  
> - **middlewares** – (пока нет)мидлвари для обработки ошибок, логирования.  


### 📁 `/dto` — Data Transfer Objects

> **Назначение:**  
> Pydantic-модели для сериализации и валидации данных, передаваемых через API.  
> Разделены на:  
> - **requests** – схемы входящих запросов (`RegisterRequest`, `UpdateRoleRequest`);  
> - **responses** – схемы ответов (`TokenResponse`, `UserResponse`).  

### Запуск приложения

1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/Elenthrill/EMS_Python_Fast_Api.git
   cd EMS_Python_Fast_Api
   ```

2. **Создайте виртуальное окружение**
   ```bash
   python -m venv venv
   source venv/bin/activate  # На Windows: venv\Scripts\activate
   ```

3. **Установите зависимости**
   ```bash
   pip install -r requirements.txt
   ```

4. **Поднимите  Dolt и Adminer с помошью докера**
   ```
   docker-compose -f docker/docker-compose.yml up
   ```

5. **Запустите приложение**
   ```
   python -m main.py
   ```

Приложение будет доступно по адресу: `http://localhost:8000`

---

## 📚 API Документация

FastAPI автоматически генерирует интерактивную документацию:

- **Swagger UI:** `http://localhost:8000/docs`

## 👤 Автор

**Elenthrill**

- GitHub: [@Elenthrill](https://github.com/Elenthrill)

</div>
