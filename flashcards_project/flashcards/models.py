from django.db import models

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
