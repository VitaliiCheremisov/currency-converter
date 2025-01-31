import os

from dotenv import load_dotenv

load_dotenv()

OPEN_EXCHANGE_RATE_API_KEY = os.getenv('OPEN_EXCHANGE_RATE_API_KEY')
OPEN_EXCHANGE_RATE_API_URL = 'https://api.exchangeratesapi.io/v1/'
EXCHANGE_RATE_API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
EXCHANGE_RATE_API_URL = (f'https://v6.exchangerate-api.com/v6/'
                         f'{EXCHANGE_RATE_API_KEY}/latest/')
CONVERSION_PARAMETERS = ('from', 'to', 'amount')
LETTER_CODES_OF_AVAILABLE_CURRENCIES = ('USD', 'EUR', 'RUB', 'CNY', 'GBP',
                                        'BYN', 'KZT', 'KGS', 'MDL', 'TMT',
                                        'AMD', 'AZN', 'UZS', 'CHF', 'CZK',
                                        'ZAR', 'BGN', 'HUF', 'AUD', 'INR',
                                        'TRY', 'THB', 'DKK', 'RON', 'NOK',
                                        'JPY', 'SGD', 'AED', 'SEK', 'CAD')
BASE_HISTORY_CURRENCY_LETTER_CODE = 'EUR'
RUB_LETTER_CODE = 'RUB'
SETTINGS_DEBUG = 'True'
BASE_EXCHANGE_RATE_ROUND_VALUE = 6
CURRENCY_NAME_MAX_LENGTH = 50
CURRENCY_SHORT_NAME_MAX_LENGTH = 3
CURRENCY_SYMBOL_MAX_LENGTH = 15
CONVERSION_RATES_MAX_DIGITS = 999
CONVERSION_RATES_DECIMAL_PLACES = BASE_EXCHANGE_RATE_ROUND_VALUE
CURRENCY_MISSING_PARAM_ERROR_MESSAGE = ('Отсутствует один или несколько '
                                        'обязательных параметров!')
AMOUNT_PARAM_ERROR_MESSAGE = ('Поле "amount" получило неожиданное значение')
