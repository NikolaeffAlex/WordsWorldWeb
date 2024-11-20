from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Card
from .serializers import CardSerializer
from django.shortcuts import render

class CardListAPI(APIView):
    def get(self, request):
        topic = request.query_params.get('topic')  # Получаем тему из параметров запроса
        if topic:
            cards = Card.objects.filter(topic=topic)
        else:
            cards = Card.objects.all()
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)

def index(request):
    return render(request, 'flashcards/index.html')

def topics(request):
    return render(request, 'flashcards/topics.html')

def cards(request):
    topic = request.GET.get('topic', None)
    return render(request, 'flashcards/cards.html', {'topic': topic})
