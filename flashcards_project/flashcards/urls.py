from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('cards/', views.cards, name='cards'),
    path('api/cards/', views.CardListAPI.as_view(), name='card-list'),
    path('training/', views.training, name='training'),
    path('register/', views.register, name='register'),
    path('progress/', views.progress_view, name='progress'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
