# Стандартные библиотеки
import random
import json
from urllib.parse import unquote

# Сторонние библиотеки
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView

# Локальные модули
from .models import Card, Topic, UserProgress
from .serializers import CardSerializer
from .forms import RegistrationForm


# Страница регистрации
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('topics')  # Перенаправление на страницу тем
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

# Страница входа
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')  # Перенаправление на профиль
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Страница выхода
def user_logout(request):
    logout(request)
    return redirect('login')  # Перенаправление на страницу входа

# Профиль пользователя
@login_required
def profile(request):
    return render(request, 'registration/profile.html')


@login_required
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

    # Разделяем карточки по типам, добавляем id
    info_cards = [{'id': card.id, 'type': 'info', 'word': card.word, 'transcription': card.transcription, 'translation': card.translation} for card in cards]
    input_cards = [{'id': card.id, 'type': 'input', 'translation': card.translation, 'word': card.word} for card in cards]
    choice_cards = [{'id': card.id, 'type': 'choice', 'word': card.word, 'translation': card.translation} for card in cards]

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


def login_view(request):
    next_url = request.GET.get('next', '/topics/')  # Если нет next, перенаправляем на /topics/
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'



"""@login_required
def progress_view(request):
    progress, created = UserProgress.objects.get_or_create(user=request.user)
    print(progress.correct_answers, progress.total_answers, progress.accuracy)  # Debugging
    return render(request, 'flashcards/progress.html', {'progress': progress})


@login_required
def update_progress(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            card_id = data.get('card_id')
            correct = data.get('correct')

            # Отладочный вывод
            print(f"Received card_id: {card_id}, correct: {correct}")

            card = Card.objects.get(id=card_id)
            progress, created = UserProgress.objects.get_or_create(user=request.user)

            if correct:
                progress.correct_answers += 1
            progress.total_answers += 1
            progress.completed_cards.add(card)
            progress.save()

            # Отладочный вывод
            print(f"Updated progress: {progress.correct_answers}/{progress.total_answers}")

            return JsonResponse({'status': 'success', 'progress': progress.accuracy})
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
"""
