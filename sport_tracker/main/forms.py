from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """Форма регистрации пользователя."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class SignInForm(AuthenticationForm):
    """Форма входа пользователя."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "login"}
        )  # Добавляем класс
        self.fields["password"].widget.attrs.update({"class": "password"})