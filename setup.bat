@echo off
echo Создание структуры проекта...

REM Создание виртуального окружения для Python
python -m venv venv
call venv\Scripts\activate
pip install flake8 isort black

REM Создание React приложения для первого задания
cd 01_frontend_github-issues
call npx create-react-app frontend --template typescript
cd ..

echo Структура создана успешно!
pause