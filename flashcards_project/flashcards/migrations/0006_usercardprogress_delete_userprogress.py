# Generated by Django 5.1.3 on 2024-12-10 13:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0005_userprogress_delete_progress'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCardProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('not_learned', 'Не выучено'), ('repeat', 'Нуждается в повторении'), ('learned', 'Выучено')], default='not_learned', max_length=20)),
                ('correct_streak', models.IntegerField(default=0)),
                ('total_attempts', models.IntegerField(default=0)),
                ('mistakes', models.IntegerField(default=0)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flashcards.card')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='UserProgress',
        ),
    ]
