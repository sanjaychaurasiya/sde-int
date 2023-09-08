# views.py
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from conversionapp.models import CurrencyRate
from .serializers import CurrencyRateSerializer
import requests


class CurrencyConversion(APIView):
    def get(self, request, from_currency, to_currency):
        # Check if the conversion rate is already in the database
        try:
            rate = CurrencyRate.objects.get(from_currency=from_currency, to_currency=to_currency)
        except CurrencyRate.DoesNotExist:
            # If the rate is not in the database, fetch it from the external API
            url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{from_currency}/{to_currency}.json"
            response = requests.get(url)

            if response.status_code != 200:
                return Response({"error": "Unable to fetch conversion rate"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            data = response.json()
            rate_value = data.get("rates", {}).get(to_currency)

            if rate_value is None:
                return Response({"error": "Conversion rate not found in API response"},
                                status=status.HTTP_404_NOT_FOUND)

            # Save the conversion rate in the database
            rate = CurrencyRate(from_currency=from_currency, to_currency=to_currency, rate=rate_value)
            rate.save()

        # Return the conversion rate
        serializer = CurrencyRateSerializer(rate)
        return Response(serializer.data)
