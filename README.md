Для установки необходимо выполнить следующую команду

pip install -r requirements.txt --update

Для загрузки тестовых данных написать

python seed.py

Для запуска api выполнить следующую команду

uvicorn main:app --reload

после можно открывать автоматическую документацию

127.0.0.1:8000/docs