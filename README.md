# finam_rest_client
Асинхронный клиент для взаимодействия с [REST API Finam](https://finamweb.github.io/trade-api-docs/).

---
## Требования
Python >= 3.12

---
## Зависимости
Установить зависимости можно через [poetry](https://python-poetry.org/docs/) или pip:
```commandline
poetry sync install --without test,dev
```
```commandline
pip install -r requirements.txt
```

---
## Тестирование
В модуле finam_rest_client.test доступны тесты для запросов к Api.

__Важно__: 
- Тестируется взаимодействие клиента с Api, а не классы и функции приложения, 
поэтому для запуска тестов необходимо интернет подключение и наличие токена 
доступа и идентификатора счета.
- Во время тестов на создание ордеров (test_order_create_and_cancel.py, 
test_stop_create_and_cancel.py) будут выставляться заявки, поэтому для их 
успешного прохождения нужно, чтобы на счете была некоторая сумма. 
Достаточно 500 рублей.

Библиотеки для запуска тестов можно установить с помощью [poetry](https://python-poetry.org/docs/) или pip:
```commandline
poetry sync install with test
```
```commandline
pip install -r requirements-test.txt
```
Для тестирования используется [pytest](https://docs.pytest.org/en/stable/index.html).