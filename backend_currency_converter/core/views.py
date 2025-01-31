import datetime as dt
import json

import requests
from dateutil.relativedelta import relativedelta
from django.db.models import Max
from django.shortcuts import get_object_or_404

from core import constants as const
from core.validators import validate_currency_param
from currencies.models import Currency, ExchangeRate


def get_conversion_rates(
        currency_letters_code: str,
        return_response_data: bool = False,
        inverse_rates: bool = False
) -> dict[str | int]:
    """Return conversion rates for a given currency.

    This service is used to obtain up-to-date data:
    Exchange-Rate API: https://www.exchangerate-api.com/docs/ .
    """
    url = get_url_to_conversion_rates(const.EXCHANGE_RATE_API_URL,
                                      currency_letters_code)
    response = send_request_and_serialize_response(url)
    if response.get('result', None) == 'success':
        if return_response_data:
            return response
        conversion_rates = response['conversion_rates']
        if inverse_rates:
            conversion_rates = inverse_conversion_rates(conversion_rates)
        return conversion_rates


def inverse_conversion_rates(conversion_rates: dict[str, int]):
    inverse_rates = {}
    for currency, conversion_rate in conversion_rates.items():
        inverse_rate = 1 / conversion_rate
        inverse_rates[currency] = inverse_rate
    return inverse_rates


def get_url_to_conversion_rates(url, base_currency):
    return f'{url}{base_currency}'


def send_request_and_serialize_response(url):
    response = requests.get(url)
    response = response.text
    response = json.loads(response)
    return response


def convert_currencies(
        target_currency,
        conversion_rates, amount
):
    conversion_rate = conversion_rates[target_currency]
    return (round(amount * conversion_rate,
                  const.BASE_EXCHANGE_RATE_ROUND_VALUE))


def get_exchange_rate_from_a_month_ago(
    currency_letter_code,
    available_currencies
):
    """Return conversion rates from a month ago for a given currency.

    This service is used to obtain historical data:
    Exchange-Rate API: https://exchangeratesapi.io/documentation/.
    When working with a free tariff, the service does not allow
    to change the base currency (default: EUR).
    """
    month_ago_date = get_a_date_month_ago()
    month_ago_exchange_rate = get_historical_exchange_rate(
        currency_letter_code,
        month_ago_date,
        available_currencies=available_currencies,
        inverse_rates=False
    )
    return month_ago_exchange_rate


def get_historical_exchange_rate(
        currency_letter_code,
        date,
        available_currencies,
        inverse_rates=False
) -> dict[str, int]:
    url = get_history_url(
        const.OPEN_EXCHANGE_RATE_API_URL, date
    )
    response = send_request_and_serialize_response(url)
    if response['success']:
        eur_conversion_rates = response['rates']
        if currency_letter_code == const.BASE_HISTORY_CURRENCY_LETTER_CODE:
            return eur_conversion_rates
        conversion_rates = get_cross_rates(
            currency_letter_code,
            eur_conversion_rates,
            available_currencies=available_currencies,
            inverse_rates=inverse_rates
        )
        return conversion_rates


def get_cross_rates(
        currency_of_target_rates: str,
        intermediate_rates: dict[str: int],
        available_currencies,
        inverse_rates: bool = False
) -> dict[str, int]:
    """Return default or inverse cross conversion rates."""
    cross_rates = {}
    for currency in available_currencies:
        cross_rate = get_cross_rate(
            currency_of_target_rates,
            currency.short_name,
            intermediate_rates,
            inverse_rate=inverse_rates
        )
        cross_rates[currency.short_name] = cross_rate
    return cross_rates


def get_cross_rate(
        source_currency: str,
        target_currency: str,
        intermediate_rates: dict[str: int],
        inverse_rate: bool = False
) -> float:
    """Return default or reverse cross conversion rate."""
    source_intermediate_rate = intermediate_rates[source_currency]
    target_intermediate_rate = intermediate_rates[target_currency]
    if inverse_rate:
        cross_rate = target_intermediate_rate / source_intermediate_rate
    else:
        cross_rate = source_intermediate_rate / target_intermediate_rate
    return cross_rate


def get_history_url(
        base_url, date
):
    return (f'{base_url}{date}?access_key={const.OPEN_EXCHANGE_RATE_API_KEY}')


def parse_currencies_query_params(
        currencies_params
) -> dict[str: str | list[str]]:
    """Extracts currency codes from "currencies" query parameter."""

    source_currency = currencies_params[0:3]
    validate_currency_param(source_currency)
    currencies = {
        'source_currency': currencies_params[0:3],
    }
    left_index = 3
    target_currencies = []
    while left_index < len(currencies_params):
        right_index = left_index + 3
        target_currency = currencies_params[left_index: right_index]
        validate_currency_param(target_currency)
        target_currencies.append(target_currency)
        left_index = right_index
    currencies['target_currencies'] = target_currencies
    return currencies


def get_history_exchange_rate_by_period(
        source_currency_short_name: str,
        target_currency_short_name: str,
        time_period: str
):
    source_currency = get_object_or_404(
        Currency.objects,
        short_name=source_currency_short_name
    )
    target_currency = get_object_or_404(
        Currency.objects,
        short_name=target_currency_short_name
    )
    last_relevant_date = get_datetime_in_past(time_period=time_period)
    relevant_exchange_rates = ExchangeRate.objects.filter(
        source_currency=source_currency,
        target_currency=target_currency,
        from_date__gte=last_relevant_date
    ).order_by('from_date').select_related('target_currency')
    return relevant_exchange_rates


def get_exchange_rate_last_update():
    last_update = ExchangeRate.objects.aggregate(Max(
        'from_date')
    )['from_date__max']
    return last_update


def get_datetime_in_past(time_period, current_date=None):
    if current_date is None:
        current_date = dt.datetime.now()
    if time_period == '12 часов':
        past_date = current_date + relativedelta(hours=-12)
    elif time_period == '1 день':
        past_date = current_date + relativedelta(months=-1)
    elif time_period == 'Неделя':
        past_date = current_date + relativedelta(days=7)
    elif time_period == 'Месяц':
        past_date = current_date + relativedelta(months=-1)
    else:
        past_date = current_date + relativedelta(years=-1)
    return past_date


def get_a_date_month_ago(current_date=None):
    if current_date is None:
        current_date = dt.datetime.now()
    month_ago_date = current_date + relativedelta(months=-1)
    return month_ago_date.date()
