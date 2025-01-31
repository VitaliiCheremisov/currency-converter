import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from core import constants as const
from currencies.models import Currency


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class CurrencySerializer(serializers.ModelSerializer):
    flag = Base64ImageField(
        read_only=True, required=False, allow_null=True
    )
    exchange_rate = serializers.SerializerMethodField(
        read_only=True,
    )
    er_dynamics = serializers.SerializerMethodField(
        read_only=True,
    )

    class Meta:
        model = Currency
        fields = ('id', 'name', 'short_name', 'symbol', 'flag',
                  'exchange_rate', 'er_dynamics')
        read_only_fields = ('id', 'name', 'short_name', 'symbol', 'flag',
                            'exchange_rate', 'er_dynamics')

    def get_exchange_rate(self, obj):
        """Actual exchange rate of currency againts RUB."""
        to_rub_conversion_rate = self.context.get(
            'rub_conversion_rates'
        ).get(obj.short_name, 0)
        return (round(
            to_rub_conversion_rate, const.BASE_EXCHANGE_RATE_ROUND_VALUE)
        )

    def get_er_dynamics(self, obj):
        """Change in the exchange rate against the RUB over the past month."""
        to_rub_conversion_rate = self.context.get(
            'rub_conversion_rates'
        ).get(obj.short_name, 0)
        to_rub_conversion_rate_month_ago = self.context.get(
            'rub_conversion_rates_month_ago'
        ).get(obj.short_name, 0)
        return (round(
            to_rub_conversion_rate - to_rub_conversion_rate_month_ago, 6)
        )
