# Stripe shop

## RU

### Способ запуска

> Для начала нужно зайти в ```docker-compose.yml``` и вписать свои ключи от Stripe. После прописать ```docker-compose build``` для сбора образа. Запуск проекта будет через ```docker-compose up``` и сервер будет стоять на *localhost:8000* . Тесты будут проведены автоматически. Зайдите в админ панель и создайте все модели, которые вам нужны. Логин: *admin*, Пароль: *qwerty*

### Launch method

> First you need to go to ``docker-compose.yml`` and enter your keys from Stripe. After that, write ``docker-compose build`` to collect the image. The project will be launched via ``docker-compose up`` and the server will be on *localhost:8000* . The tests will be performed automatically. Go to the admin panel and create all the models you need. Login: *admin*, Password: *qwerty*

# Endpoints

-- http://localhost:8000/admin - Admin panel
-- http://localhost:8000/buy/<id> - GET Stripe item id
-- http://localhost:8000/item/<id> - Get item info
-- http://localhost:8000/buy/order/<id> - GET Stripe order id
-- http://localhost:8000/order/<id> - Get order info
