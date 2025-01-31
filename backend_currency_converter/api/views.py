from rest_framework.decorators import api_view
from rest_framework.views import Response, status

from api.serializers import CurrencySerializer
from core import constants as const
from core.validators import validate_amount
from core.views import (convert_currencies, get_conversion_rates,
                        get_exchange_rate_from_a_month_ago,
                        get_exchange_rate_last_update,
                        get_history_exchange_rate_by_period,
                        parse_currencies_query_params)
from currencies.models import Currency


@api_view(['GET'])
def currencies(request):
    """Return all avalable currencies.

    Return all avalable to conversion currencies.
    The administrator creates necessary currency objects on the admin site.
    Each currency object in the serialized response contains extra feilds:
    1) "exchange_rate" is the rate for converting any currency into RUB.
    2) "er_dynamics" is a change in the exchange rate of a currency
    against the RUB over the past month.
    """
    if request.method == 'GET':
        currencies = Currency.objects.all()
        rub_conversion_rates = get_conversion_rates(const.RUB_LETTER_CODE,
                                                    inverse_rates=True)
        rub_conversion_rates_month_ago = get_exchange_rate_from_a_month_ago(
            const.RUB_LETTER_CODE,
            available_currencies=currencies
        )
        context = {
            'rub_conversion_rates': rub_conversion_rates,
            'rub_conversion_rates_month_ago': rub_conversion_rates_month_ago
        }
        serializer = CurrencySerializer(
            currencies, many=True, context=context
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
        {'error': 'Запрос не может быть обработан'},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
def conversion(request):
    """Convert one currency to another currency.

    The currencies are retrieved from the "currencies" query parameter.
    Currencies are displayed in the currencies parameter
    as a continuous string, where the first three letters always
    is source currency and next letters with slices by three letters
    is target currency.
    For example:
    1) USDRUB - convert USD to RUB.
    2) USDRUBEURNOK - convert USD to RUB, EUR and NOK.
    """
    if request.method == 'GET':
        currencies_params = request.GET.get('currencies', None)
        currencies_query_params = parse_currencies_query_params(
            currencies_params
        )
        amount = validate_amount(request.GET.get('amount', None))
        source_currency = currencies_query_params['source_currency']
        conversion_rates = get_conversion_rates(source_currency)
        conversion_results = []
        for target_currency in currencies_query_params['target_currencies']:
            conversion_result = convert_currencies(
                target_currency, conversion_rates,
                amount
            )
            conversion_results.append(conversion_result)
        return Response(conversion_results, status=status.HTTP_200_OK)
    return Response(
        {'error': 'Запрос не может быть обработан.'},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
def history(request):
    """Return the rate history for a certain period of time.

    At the moment, it is not possible to obtain historical sections
    through third-party services due to the lack of a paid subscription.
    Methods for collecting the necessary data to store it locally
    have not been found.
    Therefore, at the moment, history is simulative endpoint,
    which is necessary to demonstrate the capabilities of the frontend
    (rendering graphs displaying the dynamics of the rate).
    It is assumed that the administrator manually adds
    some data on historical rates through the admin site.
    This data, taking into account the time_period parameter,
    is returned by the endpoint.
    """
    if request.method == 'GET':
        currencies_query_params = parse_currencies_query_params(
            request.GET.get('currencies', None)
        )
        source_currency = currencies_query_params['source_currency']
        target_currency = currencies_query_params['target_currencies'][0]
        time_period = request.GET.get('time_period', None)
        relevant_exchange_rates = get_history_exchange_rate_by_period(
            source_currency, target_currency, time_period
        )
        data = []
        for exchange_rate in relevant_exchange_rates:
            data.append(
                [exchange_rate.conversion_rate,
                 exchange_rate.target_currency.short_name]
            )
        date = get_exchange_rate_last_update()
        result = {
            'data': data,
            'date': date
        }
        return Response(result, status=status.HTTP_200_OK)
    return Response(
        {'error': 'Запрос не может быть обработан.'},
        status=status.HTTP_400_BAD_REQUEST
    )
