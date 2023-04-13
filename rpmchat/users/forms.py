from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    """Форма регистрации пользователя."""

    class Meta:
        """Разметка формы."""

        model = User
        fields = ('username', 'password1', 'password2')


class CustomLoginForm(AuthenticationForm):
    """Форма авторизации пользователя."""

    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
