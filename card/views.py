from typing import Union
from django.http import JsonResponse, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Card, Order
from .services import card_change_status, search, generate_cards


def card_list(request) -> HttpResponse:
    """ Страница просмотра всех карт """

    context = {
        'cards': Card.objects.all()
    }
    return render(request, 'card_list.html', context)


def card_detail(request, card_id: int) -> HttpResponse:
    """ Страница отдельной карты """
    card = get_object_or_404(Card, id=card_id)

    context = {
        'card': card,
        'orders': Order.objects.filter(card=card)
    }
    return render(request, 'card_detail.html', context)


def card_delete(request, card_id: int) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect]:
    """ Удаление карты """
    card = get_object_or_404(Card, id=card_id)
    card.delete()
    return redirect('card:card_list')


def card_activation(request) -> JsonResponse:
    """ Смена статуса карты """
    result = card_change_status(request.POST.get('card'))
    return JsonResponse({
        'changed_to': result
    })


def search_cards(request) -> Union[HttpResponse, JsonResponse]:
    """ Поиск карт """
    series = request.GET.get('series')
    release_date = request.GET.get('release_date')
    exp_date = request.GET.get('exp_date')
    status = request.GET.get('status')
    if 'status' in request.GET:
        query = search(status=status, series=series, exp_date=exp_date, release_date=release_date)
        return JsonResponse({
            'cards': query
        })
    return render(request, 'search_cards.html')


def generate_cards_view(request) -> HttpResponse:
    """ Генерирование карт """
    if request.POST:
        generate_cards(request.POST.get('series'), request.POST.get('num_cards'), request.POST.get('exp_date'))
    return render(request, 'generate_cards.html')
