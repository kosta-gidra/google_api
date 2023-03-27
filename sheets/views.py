from pprint import pprint
import xml.etree.ElementTree as ET
import gspread
import requests

from django.http import JsonResponse
from django.views import View
from datetime import datetime, timedelta
from sheets.models import Order, Currency


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


class ReadSheetView(View):
    """Получить данные из google sheets и внести их в БД"""

    def get(self, request, *args, **kwargs):
        # проверка текущего курса доллара
        course, created = Currency.objects.get_or_create(id=1)
        if created or course.date != datetime.now().date():
            current_course = get_current_course()

            if current_course['status']:
                course.usd = current_course['dollar']
                course.date = datetime.now().date()
                course.save()

        # получение данных из google sheet
        ser_acc = gspread.service_account(filename='credential.json')
        sheet = ser_acc.open('canalservice').sheet1

        # обновление БД из google sheet
        for order in sheet.get_all_records():
            order_obj, _ = Order.objects.update_or_create(external_id=order['заказ №'],
                                                          defaults={
                                                              'coast_cents': order['стоимость,$']*100,
                                                              'delivery_date':
                                                                  datetime.strptime(order['срок поставки'], '%d.%m.%Y'),
                                                              'coast_rub': order['стоимость,$']*course.usd*100,
                                                              'status': 'active',
                                                              'last_update': datetime.now()
                                                          })

        # заказы, которые удаляются из google sheet, переходят в статус "устарел" в БД спустя 2 минуты после удаления
        timeout = datetime.now() - timedelta(minutes=2)
        old_orders = Order.objects.filter(last_update__lt=timeout)
        for order in old_orders:
            order.status = 'outdated'
            order.save()

        return JsonResponse({
            'status': 'ok'
        })
