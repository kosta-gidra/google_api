from django.db import models

CHOICES = (
    ('active', 'активен'),
    ('outdated', 'устарел')
)


class Currency(models.Model):
    usd = models.FloatField(null=True, verbose_name='курс доллара к рублю')
    date = models.DateField(auto_now_add=True, verbose_name='дата курса')


class Order(models.Model):
    external_id = models.PositiveIntegerField(verbose_name='внешний id заказа')
    coast_cents = models.PositiveIntegerField(verbose_name='стоимость в центах')
    delivery_date = models.DateField(verbose_name='срок поставки')
    coast_rub = models.PositiveIntegerField(verbose_name='стоимость в копейках')

    status = models.CharField(verbose_name='Статус заказа', choices=CHOICES, max_length=8)
    last_update = models.DateTimeField(auto_now_add=True, verbose_name='последнее обновление')

    def get_price_dol(self):
        """Стоимость в долларах"""
        coast_dollars = '{0:.2f}'.format(self.coast_cents / 100)
        return coast_dollars

    def get_price_rub(self):
        """Стоимость в рублях"""
        coast_rub = '{0:.2f}'.format(self.coast_rub / 100)
        return coast_rub
