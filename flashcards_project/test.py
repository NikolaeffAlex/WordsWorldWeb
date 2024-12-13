import os
import django

# Настройка Django для работы в скрипте
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flashcards_project.settings")  # Поменяй на имя своего проекта
django.setup()

from flashcards.models import Card, Topic  # Импортируем нужные модели (поменяй на свои)

def check_words_for_topic(topic_id):
    try:
        # Получаем тему по ID
        topic = Topic.objects.get(id=topic_id)
        print(f"Checking words for topic: {topic.name} (ID: {topic.id})")

        # Извлекаем все слова для этой темы
        words = Card.objects.filter(topic_id=topic_id)

        # Печатаем количество слов
        print(f"Found {len(words)} words for topic {topic_id}")

        # Печатаем первые несколько слов (для проверки)
        for word in words[:10]:  # Печатаем первые 10 слов (можно изменить количество)
            print(f"Word: {word.word}, Status: {word.status}")

    except Topic.DoesNotExist:
        print(f"Topic with ID {topic_id} does not exist.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Цикл по всем ID тем с 1 по 20
    for topic_id in range(1, 21):
        check_words_for_topic(topic_id)
