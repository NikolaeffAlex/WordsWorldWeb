# flashcards/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserCardProgress, Card
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_progress(sender, instance, created, **kwargs):
    """
    Этот сигнал срабатывает при создании нового пользователя.
    Для этого пользователя создаются статусы для всех карточек с начальным значением 'not_learned'.
    """
    if created:
        # Создаем прогресс для пользователя по всем карточкам
        cards = Card.objects.all()  # Получаем все карточки
        for card in cards:
            # Для каждой карточки создаем запись в UserCardProgress с начальным статусом
            UserCardProgress.objects.get_or_create(
                user=instance,
                card=card,
                defaults={'status': 'not_learned'}
            )
