import xml.etree.ElementTree as ET
import requests

from rest_framework.viewsets import ReadOnlyModelViewSet

from sheets.models import Order, Currency
from sheets.serializers import OrderSerializer, CurrencySerializer


def get_current_course():
    """Получить текущий курс доллара к рублю"""

    try:
        get_xml = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
        structure = ET.fromstring(get_xml.content)
        dollar = structure.find("./*[@ID='R01235']/Value")
        dollar_float = float(dollar.text.replace(',', '.'))

        return {'status': True, 'dollar': dollar_float}

    except requests.exceptions.RequestException as e:
        return {'status': False, 'errors': e}


class GetOrders(ReadOnlyModelViewSet):
    """ Класс для получения всех заказов """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class GetCurrency(ReadOnlyModelViewSet):
    """ Класс для получения текущего курса доллара """

    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
