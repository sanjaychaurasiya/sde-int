# urls.py
from django.urls import path
from .views import CurrencyConversion

urlpatterns = [
    path('convert/<str:from_currency>/<str:to_currency>/', CurrencyConversion.as_view(), name='currency-conversion'),
]
