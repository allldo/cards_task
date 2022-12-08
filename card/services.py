from datetime import datetime
import random
from datetime import date
from time import strptime

from django.db.models import Q
from rest_framework.utils.serializer_helpers import ReturnDict
from dateutil.relativedelta import relativedelta

from .models import Card
from django.shortcuts import get_object_or_404
from .serilizers import CardSerializer


def card_change_status(card_id: int) -> str:
    """ Смена статуса карты """
    card = get_object_or_404(Card, id=card_id)
    if card.status == 'ACTIVATED':
        card.status = 'NON_ACTIVATED'
        card.save()
        return 'deactivated'
    elif card.status == 'NON_ACTIVATED':
        card.status = 'ACTIVATED'
        card.save()
        return 'activated'


def search(status: str, series: str = None, exp_date: str = '', release_date: str = '') -> ReturnDict:
    """ Поиск по картам (условие И) """
    if exp_date:
        exp_date = strptime(exp_date, '%Y-%m-%d')
    if release_date:
        release_date = strptime(release_date, '%Y-%m-%d')
    query = Card.objects.filter(
        Q(status=status) & Q(series=series)
        & Q(expiration_date__year=exp_date.tm_year, expiration_date__day=exp_date.tm_mday,
            expiration_date__month=exp_date.tm_mon)
        & Q(release_date__year=release_date.tm_year, release_date__day=release_date.tm_mday,
            release_date__month=release_date.tm_mon)
    )
    serialized = CardSerializer(query, many=True).data
    return serialized


def generate_cards(series: str, num_to_gen: int, exp_date: str):
    """ Генерация карт """
    list_with_objs = []

    if exp_date == '1 год':
        exp_date = datetime.now() + relativedelta(years=1)
    elif exp_date == '6 месяцев':
        exp_date = datetime.now() + relativedelta(month=6)
    elif exp_date == '1 месяц':
        exp_date = datetime.now() + relativedelta(month=1)

    number = ''.join(random.choice('1234567890') for i in range(16))
    currency = ''.join(random.choice(['RUB', 'USD', 'KZT']) for i in range(1))
    for x in range(int(num_to_gen)):
        list_with_objs.append(Card(series=series, number=number, currency=currency, release_date=datetime.now(),
                                   expiration_date=exp_date, balance=0, status='ACTIVATED'))

    Card.objects.bulk_create(list_with_objs)
