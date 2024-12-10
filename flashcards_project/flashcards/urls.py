from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('cards/', views.cards, name='cards'),
    path('api/cards/', views.CardListAPI.as_view(), name='card-list'),
    path('training/', views.training, name='training'),
    path('update_progress/', views.update_progress, name='update_progress'),
    path('topic/<int:topic_id>/', views.topic_details, name='topic_details'),
    #path('progress/', views.progress_view, name='progress'),
    #path('update_progress/', views.update_progress, name='update_progress'),
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
