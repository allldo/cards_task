from django.utils import timezone
from celery import shared_task
from .models import Card


@shared_task()
def check_if_expired():
    """ Count and save total comments for each topic """
    for card in Card.objects.all():
        if timezone.now() > card.expiration_date:
            card.status = 'EXPIRED'
            card.save()

