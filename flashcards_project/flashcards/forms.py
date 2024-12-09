from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Форма для регистрации пользователя
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
'''
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()  # Добавляем поле для email
    first_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
'''