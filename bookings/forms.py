from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinLengthValidator
import re
from .models import Booking


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        min_length=6,
        label='Логин',
        help_text='Только латинские буквы и цифры, минимум 6 символов'
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
        label='Пароль'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label='Подтверждение пароля'
    )
    full_name = forms.CharField(max_length=255, label='ФИО')
    phone_number = forms.CharField(
        max_length=20,
        label='Номер телефона',
        widget=forms.TextInput(attrs={'placeholder': '+7 (123) 456-78-90'})
    )
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            raise forms.ValidationError('Логин должен содержать только латинские буквы и цифры')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Пароль должен содержать минимум 8 символов')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')
        if password and confirm and password != confirm:
            raise forms.ValidationError('Пароли не совпадают')


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class BookingForm(forms.ModelForm):
    conference_date = forms.DateTimeField(
        label='Дата и время начала конференции',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )

    class Meta:
        model = Booking
        fields = ['room_type', 'conference_date', 'payment_method']
        widgets = {
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['review']
        widgets = {
            'review': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Напишите ваш отзыв ...'})
        }