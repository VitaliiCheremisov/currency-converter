from django.urls import path

from api.views import conversion, currencies, history

app_name = 'api'


urlpatterns = [
    path('currencies', currencies),
    path('conversion', conversion),
    path('history', history)
]
