from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Card, Topic
from .serializers import CardSerializer
from django.shortcuts import render
from urllib.parse import unquote
import random

from urllib.parse import unquote

def training(request):
    # Получаем список выбранных тем из параметров запроса
    selected_topics = request.GET.get('topics', '')  # Получаем строку с темами
    selected_topics = unquote(selected_topics)  # Декодируем URL

    if selected_topics:  # Если строка с темами не пуста
        # Разделяем строку на отдельные темы
        selected_topics_list = [topic.strip() for topic in selected_topics.split(',')]
    else:
        selected_topics_list = []  # Если тем нет, возвращаем пустой список

    # Фильтруем карточки по выбранным темам
    if selected_topics_list:
        cards = Card.objects.filter(topic__name__in=selected_topics_list)
    else:
        cards = Card.objects.all()  # Если темы не выбраны, возвращаем все карточки

    # Преобразуем QuerySet в список, перемешиваем и ограничиваем тренировку 10 карточками
    cards = list(cards)  # Преобразуем QuerySet в список
    random.shuffle(cards)  # Перемешиваем карточки
    cards = cards[:10]  # Ограничиваем тренировку 10 карточками

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
