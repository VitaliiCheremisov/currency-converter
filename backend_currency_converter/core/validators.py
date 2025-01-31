from rest_framework.serializers import ValidationError

from core import constants as const


def validate_currency_param(currency_letter_code: str):
    if currency_letter_code not in const.LETTER_CODES_OF_AVAILABLE_CURRENCIES:
        raise ValidationError(
            {'validation-error': const.CURRENCY_MISSING_PARAM_ERROR_MESSAGE}
        )
    return currency_letter_code


def validate_amount(amount):
    try:
        return float(amount)
    except Exception:
        raise ValidationError(
            {'validation-error': const.AMOUNT_PARAM_ERROR_MESSAGE}
        )
