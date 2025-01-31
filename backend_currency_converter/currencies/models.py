from django.db import models

from core import constants as const


class Currency(models.Model):
    name = models.CharField(
        max_length=const.CURRENCY_NAME_MAX_LENGTH,
        verbose_name='Полное название валюты'
    )
    short_name = models.CharField(
        max_length=const.CURRENCY_SHORT_NAME_MAX_LENGTH,
        verbose_name='Буквенный код'
    )
    symbol = models.TextField(
        max_length=const.CURRENCY_SYMBOL_MAX_LENGTH,
        blank=True,
        null=True,
        verbose_name='Код символа валюты в формате HTML'
    )
    # flag = models.ImageField(
    #     upload_to='currencies/flags/images/',
    #     null=True,
    #     blank=True,
    #     default=None,
    #     verbose_name='Картинка валюты в формате svg'
    # )
    flag = models.FileField(
        upload_to='currencies/flags/images/',
        null=True,
        blank=True,
        default=None,
        verbose_name='Картинка валюты в формате svg'
    )

    class Meta:
        ordering = ('short_name', 'name')
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'

    def __str__(self):
        return f'{self.name} ({self.short_name})'


class ExchangeRate(models.Model):
    source_currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE,
        null=False,
        related_name='exchange_rate_source',
        verbose_name='исходная валюта'
    )
    target_currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE,
        null=False,
        related_name='exchange_rate_target',
        verbose_name='целевая валюта'
    )
    conversion_rate = models.DecimalField(
        max_digits=const.CONVERSION_RATES_MAX_DIGITS,
        decimal_places=const.CONVERSION_RATES_DECIMAL_PLACES,
        verbose_name='Курс обмена'
    )
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()

    class Meta:
        ordering = ('from_date', 'source_currency')
        verbose_name = 'курс обмена'
        verbose_name_plural = 'курсы обмена'

    def __str__(self):
        return f'Курс {self.source_currency}: {self.target_currency}'
