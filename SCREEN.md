# Скриншоты работающего приложения

## 1. Админ-панель Django
![Admin Panel](screenshots/admin_panel.png)
*Рисунок 1 - Главная страница административной панели Django*

## 2. API ответ с данными сотрудников
![API Response](screenshots/api_response.png)
*Рисунок 2 - JSON ответ от API /api/team/get_employees/ с тестовыми данными*

## 3. Запущенный сервер
![Server Running](screenshots/server_running.png)
*Рисунок 3 - Консоль с запущенным Django сервером*

## Структура проекта
01_backend_fitnesskit_employee_api/
├── api/
│ ├── migrations/
│ │ └── init.py
│ ├── init.py
│ ├── urls.py
│ └── views.py
├── config/
│ ├── init.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── screenshots/
│ ├── admin_panel.png
│ ├── api_response.png
│ └── server_running.png
├── .env.example
├── .gitignore
├── manage.py
├── README.md
├── requirements.txt
├── SCREEN.md
└── TASK.md

## Инструкция по созданию скриншотов

### Скриншот 1: Админ-панель
1. Запустите сервер: `python manage.py runserver`
2. Откройте браузер: http://127.0.0.1:8000/admin
3. Войдите: логин `admin`, пароль `admin123`
4. Нажмите `Alt + PrtScn` (скриншот активного окна)
5. Сохраните как `screenshots/admin_panel.png`

### Скриншот 2: API ответ
1. Откройте новую вкладку: http://127.0.0.1:8000/api/team/get_employees/
2. Нажмите `Alt + PrtScn`
3. Сохраните как `screenshots/api_response.png`

### Скриншот 3: Сервер
1. Переключитесь на окно консоли с запущенным сервером
2. Нажмите `Alt + PrtScn`
3. Сохраните как `screenshots/server_running.png`

## Примечание
Сервер 1С временно недоступен, поэтому в API используются тестовые данные для демонстрации формата ответа. Код для реальной интеграции с 1С готов и находится в `api/views.py`.
