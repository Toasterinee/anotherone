Для локального запуска удалить папку виртуального пространства .venv и пересоздать ее этими командами:

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

Восстановление базы данных из дампа:

psql -U faspapi_user -h localhost -d myfastapidb -f backup.dump

Запуск локального сервера через эту команду:

uvicorn app.main:app