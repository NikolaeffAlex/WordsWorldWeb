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
        return self.wordcl

class UserProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    correct_answers = models.IntegerField(default=0)
    total_answers = models.IntegerField(default=0)
    completed_cards = models.ManyToManyField(Card)

    @property
    def accuracy(self):
        if self.total_answers == 0:
            return 0
        return (self.correct_answers / self.total_answers) * 100

    def __str__(self):
        return f"{self.user.username}'s Progress"
