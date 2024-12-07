from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Card, Topic
from .serializers import CardSerializer
from django.shortcuts import render
from urllib.parse import unquote
import random
import json

from urllib.parse import unquote

def training(request):
    # Получаем список выбранных тем из параметров запроса
    selected_topics = request.GET.get('topics', '')  # Получаем строку с темами
    selected_topics = unquote(selected_topics).split(',')  # Разделяем темы

    if selected_topics:
        cards = Card.objects.filter(topic__name__in=selected_topics)
    else:
        cards = Card.objects.all()  # Если темы не выбраны, возвращаем все карточки

    # Преобразуем QuerySet в список, перемешиваем и ограничиваем тренировку 10 карточками
    cards = list(cards)  # Преобразуем QuerySet в список
    random.shuffle(cards)  # Перемешиваем карточки
    cards = cards[:10]  # Ограничиваем тренировку 10 карточками

    # Разделяем карточки по типам
    info_cards = [{'type': 'info', 'word': card.word, 'transcription': card.transcription, 'translation': card.translation} for card in cards]
    input_cards = [{'type': 'input', 'translation': card.translation, 'word': card.word} for card in cards]
    choice_cards = [{'type': 'choice', 'word': card.word, 'translation': card.translation} for card in cards]

    # Объединяем карточки с разными типами
    training_data = []
    while info_cards or input_cards or choice_cards:
        card_type = random.choice(['info', 'input', 'choice'])

        if card_type == 'info' and info_cards:
            training_data.append(info_cards.pop())
        elif card_type == 'input' and input_cards:
            training_data.append(input_cards.pop())
        elif card_type == 'choice' and choice_cards:
            training_data.append(choice_cards.pop())

    # Передаем карточки в шаблон
    return render(request, 'flashcards/training.html', {'cards': json.dumps(training_data)})






def topics(request):
    topics = Topic.objects.all()  # Получаем все темы из базы
    return render(request, 'flashcards/topics.html', {'topics': topics})


class CardListAPI(APIView):
    def get(self, request):
        topics = request.query_params.getlist('topic')  # Получаем список тем
        if topics:
            cards = Card.objects.filter(topic__in=topics)
        else:
            cards = Card.objects.all()
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)


def index(request):
    return render(request, 'flashcards/index.html')

def cards(request):
    topic = request.GET.get('topic', None)
    return render(request, 'flashcards/cards.html', {'topic': topic})
