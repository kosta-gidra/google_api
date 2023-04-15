from datetime import datetime, timedelta
import gspread

from google_api import settings
from google_api.celery import app
from sheets.models import Currency, Order
from sheets.views import get_current_course


@app.task
def get_google_sheet():
    course, created = Currency.objects.get_or_create(id=1)
    if created or course.date != datetime.now().date():
        current_course = get_current_course()

        if current_course['status']:
            course.usd = current_course['dollar']
            course.date = datetime.now().date()
            course.save()

    # получение данных из google sheet
    ser_acc = gspread.service_account(filename='credential.json')
    sheet = ser_acc.open(settings.SHEET_NAME).sheet1

    # обновление БД из google sheet
    for order in sheet.get_all_records():
        order_obj, _ = Order.objects.update_or_create(external_id=order['заказ №'],
                                                      defaults={
                                                          'coast_cents': order['стоимость,$'] * 100,
                                                          'delivery_date':
                                                              datetime.strptime(order['срок поставки'], '%d.%m.%Y'),
                                                          'coast_cop': order['стоимость,$'] * course.usd * 100,
                                                          'status': 'active',
                                                          'last_update': datetime.now()
                                                      })

    # заказы, которые удаляются из google sheet, переходят в статус "устарел" в БД спустя 2 минуты после удаления
    timeout = datetime.now() - timedelta(minutes=2)
    old_orders = Order.objects.filter(last_update__lt=timeout)
    for order in old_orders:
        order.status = 'outdated'
        order.save()
