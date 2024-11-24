from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('cards/', views.cards, name='cards'),
    path('api/cards/', views.CardListAPI.as_view(), name='card-list'),
    path('training/', views.training, name='training'),
]
