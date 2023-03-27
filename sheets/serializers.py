from rest_framework import serializers

from sheets.models import Order, Currency


class OrderSerializer(serializers.ModelSerializer):
    coast_dollars = serializers.FloatField(source='get_price_dol', read_only=True)
    coast_rub = serializers.FloatField(source='get_price_rub', read_only=True)

    class Meta:
        model = Order
        fields = ['external_id', 'delivery_date', 'coast_rub', 'coast_dollars', 'status']


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ['usd', 'date']
