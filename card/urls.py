from django.urls import path
from .views import card_list, card_detail, card_delete, card_activation, search_cards, generate_cards_view
app_name = 'card'

urlpatterns = [
    path('', card_list, name='card_list'),
    path('card_detail/<int:card_id>', card_detail, name='card_detail'),
    path('card_delete/<int:card_id>', card_delete, name='card_delete'),
    path('card_activation', card_activation, name='card_activation'),
    path('search_cards', search_cards, name='search_cards'),
    path('generate_cards', generate_cards_view, name='generate_cards'),
]
