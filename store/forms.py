from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import User


class RegUser(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Фамилия'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'placeholder': 'Логин'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'placeholder': 'Email'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control py-4', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control py-4', 'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control py-4',
            'placeholder': 'Введите имя пользователя'
        }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control py-4',
            'placeholder': 'Введите пароль'
        }))

    class Meta:
        model = User
        fields = ('username', 'password')


class ChangeProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}), required=False)
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': True}), required=False)
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-filee-input'}), required=False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}), required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'image', 'username', 'email']
