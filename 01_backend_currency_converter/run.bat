@echo off
echo ========================================
echo   Currency Converter API
echo ========================================
echo.

echo 1. Создание виртуального окружения...
python -m venv venv
call venv\Scripts\activate.bat
echo.

echo 2. Установка зависимостей...
pip install -r requirements.txt
echo.

echo 3. Запуск приложения...
echo.
echo Приложение будет доступно по адресу: http://localhost:8000
echo Документация Swagger: http://localhost:8000/docs
echo.
echo Для остановки нажмите Ctrl+C
echo.

uvicorn app.main:app --reload --port 8000