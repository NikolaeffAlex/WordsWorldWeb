import csv
from flashcards.models import Card, Topic


def import_words_from_csv(file_path):
    with open(file_path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Получаем или создаем тему
            topic_name = row['topic']
            topic, created = Topic.objects.get_or_create(name=topic_name)

            # Создаем карточку
            Card.objects.create(
                word=row['word'],
                translation=row['translation'],
                transcription=row['transcription'],
                topic=topic
            )
    print("Импорт завершен успешно!")

