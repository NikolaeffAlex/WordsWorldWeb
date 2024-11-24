from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Card, Topic
from .serializers import CardSerializer
from django.shortcuts import render
import random

def training(request):
    # Получаем выбранные темы из параметров запроса
    selected_topics = request.GET.getlist('topics')

    # Фильтруем карточки по выбранным темам
    if selected_topics:
        cards = Card.objects.filter(topic__name__in=selected_topics)
    else:
        cards = Card.objects.all()  # Если темы не выбраны, возвращаем все карточки

    # Ограничиваем тренировку 10 карточками
    cards = cards[:10]

    # Передаем карточки в шаблон
    return render(request, 'flashcards/training.html', {'cards': cards})



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

