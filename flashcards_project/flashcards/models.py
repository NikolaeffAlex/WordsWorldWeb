from django.db import models

class Card(models.Model):
    word = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    transcription = models.CharField(max_length=100)
    topic = models.CharField(max_length=50)

    def __str__(self):
        return self.word
