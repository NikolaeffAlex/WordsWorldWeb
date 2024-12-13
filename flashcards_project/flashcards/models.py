from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Card(models.Model):
    word = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    transcription = models.CharField(max_length=100)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='cards')

    def __str__(self):
        return self.word


class UserCardProgress(models.Model):
    STATUS_CHOICES = [
        ("learned", "Выучено"),
        ("needs_review", "Нуждается в повторении"),
        ("not_learned", "Не выучено"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="not_learned")
    correct_streak = models.IntegerField(default=0)  # Счетчик правильных ответов подряд
    mistakes = models.IntegerField(default=0)  # Количество ошибок
    total_attempts = models.IntegerField(default=0)  # Общее количество попыток

    def update_status(self, correct):
        """
        Обновляет статус карточки в зависимости от результата задания.
        """
        self.total_attempts += 1
        if correct:
            self.correct_streak += 1
            if self.correct_streak >= 5:
                self.status = "learned"
        else:
            self.correct_streak = 0
            self.mistakes += 1
            if self.status == "learned":
                self.status = "needs_review"
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.card.word} - {self.status}"


