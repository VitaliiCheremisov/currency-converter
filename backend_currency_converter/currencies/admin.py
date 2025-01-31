from django.contrib import admin

from currencies.models import Currency, ExchangeRate

admin.site.register(Currency)
admin.site.register(ExchangeRate)
