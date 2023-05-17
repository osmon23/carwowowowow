from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginForm(AuthenticationForm):
    pass


class RegistrationForm(UserCreationForm):
    pass
