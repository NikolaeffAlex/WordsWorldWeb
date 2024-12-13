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
from django.http import JsonResponse
from django.db.models import Count, Q

# Локальные модули
from .models import Card, Topic, UserCardProgress
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
    progress = UserCardProgress.objects.filter(user=request.user).order_by('status')
    return render(request, 'flashcards/profile.html', {'progress': progress})


@login_required
def training(request):
    # Получаем список выбранных тем из параметров запроса
    selected_topics = request.GET.get('topics', '')  # Получаем строку с темами
    selected_topics = unquote(selected_topics).split(',')  # Разделяем темы

    if selected_topics:
        cards = Card.objects.filter(topic__name__in=selected_topics)
    else:
        cards = Card.objects.all()  # Если темы не выбраны, возвращаем все карточки

    # Подготовка статусов карточек
    user_progress = UserCardProgress.objects.filter(user=request.user, card__in=cards).select_related('card')
    statuses = {
        "not_learned": [progress.card.word for progress in user_progress if progress.status == "not_learned"],
        "needs_review": [progress.card.word for progress in user_progress if progress.status == "needs_review"],
        "learned": [progress.card.word for progress in user_progress if progress.status == "learned"],
    }

    # Получаем тренировочный набор
    training_set = generate_training_set(statuses, total_cards=35, total_words=7)

    # Подготавливаем данные для шаблона
    training_data = []
    card_map = {card.word: card for card in cards}

    for word, card_type in training_set:
        card = card_map.get(word)
        if card:
            training_data.append({
                'id': card.id,
                'type': card_type,
                'word': card.word,
                'transcription': card.transcription,
                'translation': card.translation,
            })

    # Логирование


    if request.method == 'POST':
        # Обработка ответов
        for card_data in training_data:
            card = Card.objects.get(id=card_data['id'])
            user_progress, created = UserCardProgress.objects.get_or_create(user=request.user, card=card)

            # Получаем ответ пользователя
            user_answer = request.POST.get(f'card_{card.id}', '').strip().lower()
            correct = user_answer == card.translation.lower()

            # Обновляем статус карточки
            user_progress.update_status(correct)

        return redirect('profile')

    # Логирование: проверим, сколько карточек выбираем
    print(f"Training data length: {len(training_data)}")

    # Логирование: проверим содержимое тренировочного набора
    print(f"Training data: {training_data}")
    return render(request, 'flashcards/training.html', {'cards': json.dumps(training_data)})


def generate_training_set(statuses, total_cards=35, total_words=7):
    all_words = []
    word_status_map = {}
    training_set = []

    # Создаем плоский список слов с их статусами
    for status, words in statuses.items():
        for word in words:
            all_words.append(word)
            word_status_map[word] = status

    # Сортируем слова по статусам
    not_learned = [word for word in all_words if word_status_map[word] == "not_learned"]
    needs_review = [word for word in all_words if word_status_map[word] == "needs_review"]
    learned = [word for word in all_words if word_status_map[word] == "learned"]

    # Инициализируем список для выбранных слов
    selected_words = []

    # Шаг 1: Заполняем список выбранных слов (total_words) по категориям
    # 1. Сначала из not_learned
    selected_words.extend(random.sample(not_learned, min(len(not_learned), total_words - len(selected_words))))

    # 2. Если не хватает, берем из needs_review
    remaining_words = total_words - len(selected_words)
    selected_words.extend(random.sample(needs_review, min(len(needs_review), remaining_words)))

    # 3. Если все равно не хватает, берем из learned
    remaining_words = total_words - len(selected_words)
    selected_words.extend(random.sample(learned, min(len(learned), remaining_words)))

    # Убедимся, что у нас есть нужное количество слов
    if len(selected_words) < total_words:
        print("Warning: не хватает слов для тренировки, увеличиваем количество повторений.")
        # Заполняем недостающие слова случайным образом из доступных
        all_available_words = list(set(not_learned + needs_review + learned))
        remaining_words = total_words - len(selected_words)
        if len(all_available_words) >= remaining_words:
            selected_words.extend(random.sample(all_available_words, remaining_words))
        else:
            selected_words.extend(all_available_words)

    # Делаем случайное перемешивание выбранных слов
    random.shuffle(selected_words)

    # Шаг 2: Генерируем тренировочный набор (35 карточек)
    word_usage_count = {word: 0 for word in selected_words}
    info_shown = set()

    # Генерация набора карточек для тренировки
    while len(training_set) < total_cards:
        word = random.choice(selected_words)

        # Учитываем максимум 5 карточек на слово (1 информационная + 4 задания)
        if word_usage_count[word] < 5:
            if word not in info_shown:  # Первая карточка всегда информационная
                training_set.append((word, "info"))
                info_shown.add(word)
            else:  # После информационной карточки идут задания
                task_type = random.choice(["choose_correct_translation", "type_word"])
                training_set.append((word, task_type))

            word_usage_count[word] += 1

    return training_set


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


@login_required
def update_progress(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        card_id = data.get('card_id')
        correct = data.get('correct')

        card = Card.objects.get(id=card_id)
        user_progress, created = UserCardProgress.objects.get_or_create(user=request.user, card=card)

        user_progress.update_status(correct)

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


@login_required
def profile(request):
    # Получаем все темы
    topics = Topic.objects.all()

    # Создаем статистику только для текущего пользователя
    stats = []
    for topic in topics:
        total_words = topic.cards.count()
        learned_words = UserCardProgress.objects.filter(
            user=request.user,  # Фильтруем только по текущему пользователю
            card__topic=topic,
            status="learned"
        ).count()
        percentage = (learned_words / total_words) * 100 if total_words > 0 else 0
        stats.append({
            'topic': topic,
            'total_words': total_words,
            'learned_words': learned_words,
            'percentage': percentage
        })

    return render(request, 'flashcards/profile.html', {'stats': stats, 'user': request.user})


@login_required
def topic_details(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    words = Card.objects.filter(topic=topic)

    # Получаем статистику по словам
    word_stats = []
    for word in words:
        user_progress = word.usercardprogress_set.filter(user=request.user).first()
        status = user_progress.status if user_progress else "not_learned"
        word_stats.append({
            'word': word.word,
            'translation': word.translation,
            'status': status
        })

    return render(request, 'flashcards/topic_details.html', {'topic': topic, 'word_stats': word_stats})


