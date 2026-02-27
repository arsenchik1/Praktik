@echo off
echo ========================================
echo   Currency Converter API (Docker)
echo ========================================
echo.

echo 1. Сборка Docker образа...
docker-compose build
echo.

echo 2. Запуск контейнера...
docker-compose up -d
echo.

echo 3. Проверка статуса...
docker-compose ps
echo.

echo ========================================
echo   Приложение запущено!
echo   Адрес: http://localhost:8000
echo   Документация: http://localhost:8000/docs
echo ========================================
echo.
echo Для остановки выполните: docker-compose down