from django.forms import ModelForm, CheckboxSelectMultiple
from .models import Author, Quote
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = "__all__"


class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        fields = ["quote", "author", "tags"]
        widgets = {
            "tags": CheckboxSelectMultiple,
        }
