# Проект: Сервис для конвертации валют

*На стадии разработки.*

Веб-часть сервиса в котором вы можете отследить сколько стоят ваши деньги в другой валюте.

## Технологии:
* Python
* Django
* Django REST framework
* PostgreSQL
* Gunicorn
* Nginx
* Docker

## Адрес проекта:

**https://goconvert.zapto.org/**

## Как запустить Dev-сервер:

**Клонируйте репозиторий:**

```
git clone git@github.com:Team4-YP-CurrencyConverter/BackendCurrencyConverter.git
```

**Создайте и активируйте виртуальное окружение, установите зависимости:**
```
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

**Создайте 2 файла .env и укажите в них переменные окружения:**
```
# .../BackendCurrencyConverter/converter/.env

SECRET_KEY = ***
POSTGRES_DB = ***
POSTGRES_USER = ***
POSTGRES_PASSWORD = ***
DB_HOST = ***
DB_PORT = ***

# .../BackendCurrencyConverter/core/.env

OPEN_EXCHANGE_RATE_API_KEY = ***  # (API ACCESS KEY для внешнего сервиса: https://exchangeratesapi.io/documentation/)
EXCHANGE_RATE_API_KEY = ***  # (API ACCESS KEY для внешнего сервиса: https://www.exchangerate-api.com/docs/overview)

```

**Создайте и выполните миграции, запустите сервер для разработки:**
```
# .../CurrencyConverter/BackendCurrencyConverter/

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

```

**Создайте объекты валют, с которыми будет работать API, в админ-зоне проекта:**
```
# Создать аккаунт администратора:

python manage.py createsuperuser

```

## Доступные валюты:

При условии, что объекты валют созданы через админ-зону проекта, API будет работать с валютами, представленными ниже:

* 'USD', 'EUR', 'RUB', 'CNY', 'GBP',
* 'BYN', 'KZT', 'KGS', 'MDL', 'TMT',
* 'AMD', 'AZN', 'UZS', 'CHF', 'CZK',
* 'ZAR', 'BGN', 'HUF', 'AUD', 'INR',
* 'TRY', 'THB', 'DKK', 'RON', 'NOK',
* 'JPY', 'SGD', 'AED', 'SEK', 'CAD'

### Чтобы расширить список доступных валют:

* проверьте что новая валюта поддерживается сторонними сервисами:
1) https://www.exchangerate-api.com/docs/overview 
2) https://exchangeratesapi.io/documentation/
* добавьте валюту в переменную LETTER_CODES_OF_AVAILABLE_CURRENCIES (.../BackendCurrencyConverter/core/constants.py)
