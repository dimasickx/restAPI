# Деплой на heroku
### Установка клиента
### Создаем приложение:
``` heroku create ```
### Создадим db heroku:
```heroku addons:create heroku-postgresql```
### Создадим Procfile для указания способа запуска нашего приложение и пропишем там: 
```web: gunicorn app.wsgi --log-file -```
### Запушем приложение в хероку:
```git push heroku master```

##### https://radiant-headland-74346.herokuapp.com/catalog/
