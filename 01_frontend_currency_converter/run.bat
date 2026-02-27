@echo off
echo ========================================
echo   Frontend Currency Converter
echo ========================================
echo.
echo Выберите способ запуска:
echo 1. Открыть в браузере (простой)
echo 2. Запустить через Python сервер
echo 3. Запустить через Docker
echo.

set /p choice="Введите номер (1-3): "

if "%choice%"=="1" (
    echo Открываем index.html...
    start index.html
)

if "%choice%"=="2" (
    echo Запускаем Python сервер на порту 3000...
    start http://localhost:3000
    python -m http.server 3000
)

if "%choice%"=="3" (
    echo Собираем Docker образ...
    docker build -t currency-converter .
    echo Запускаем контейнер...
    docker run -d -p 8080:80 --name currency-app currency-converter
    echo Приложение доступно: http://localhost:8080
    start http://localhost:8080
)