from django.db import models
from django.urls import reverse


class Card(models.Model):
    """ Модель карты """
    CARD_CHOICES = (
        ('NON_ACTIVATED', 'not activated'),
        ('ACTIVATED', 'activated'),
        ('EXPIRED', 'expired'),
    )

    CURRENCY_CHOICES = (
        ('RUB', 'RUB'),
        ('USD', 'USD'),
        ('KZT', 'KZT'),
    )

    series = models.CharField(max_length=35, verbose_name='Серия')
    number = models.CharField(max_length=16, verbose_name='Номер')
    release_date = models.DateTimeField(verbose_name='Дата выпуска')
    expiration_date = models.DateTimeField(verbose_name='Дата истечения')
    last_usage_date = models.DateTimeField(verbose_name='Дата последнего использования', null=True, blank=True)
    balance = models.FloatField(default=0.0, verbose_name='Баланс')
    status = models.CharField(choices=CARD_CHOICES, max_length=35, verbose_name='Статус')
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=35, verbose_name='Валюта')

    def __str__(self):
        return self.number

    def get_absolute_url(self):
        """ Получение адреса для каждой карты """
        return reverse('card:card_detail', args=[self.pk])


class Item(models.Model):
    """ Модель предмета дял покупки """
    name = models.CharField(max_length=255)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    """ Модель объединения товаров в заказ """
    items = models.ManyToManyField('card.Item', blank=False, verbose_name='Товары')
    paid = models.BooleanField(default=False)
    card = models.ForeignKey('card.Card', on_delete=models.SET_NULL, null=True, blank=True)
