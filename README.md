# Деплой на heroku
Установка клиента
Создаем приложение: heroku create
Запушем приложение в хероку: git push heroku master
Создадим db heroku: heroku addons:create heroku-postgresql
Создадим Procfile для указания способа запуска нашего приложение и пропишем там: 
web: gunicorn app.wsgi --log-file -
