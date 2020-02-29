
from django import forms
from django.forms import HiddenInput, PasswordInput, ModelForm


from ratings.models import Ratings

RECOMMEND = (
    (1, 'Tak'),
    (2, 'Nie')
)

class LoginForm(forms.Form):
    login = forms.CharField(label="Podaj login", required=False)
    password = forms.CharField(label="Podaj hasło", widget=PasswordInput, required=False)


class RegisterForm(forms.Form):
    login = forms.CharField(label="Podaj login")
    password = forms.CharField(label="Podaj hasło", widget=PasswordInput)
    second_password = forms.CharField(label="Powtórz hasło", widget=PasswordInput)
    email = forms.EmailField(label="Podaj email")

class SearchShowForm(forms.Form):
    show_title = forms.CharField(label="Podaj tytuł", max_length=100)

class RateForm(ModelForm):
    class Meta:
        model = Ratings
        fields = ["rating", "comment"]
    recommend = forms.ChoiceField(label="Dodaj do polecanych", choices=RECOMMEND)