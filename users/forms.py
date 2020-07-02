from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 50, 'style': 'resize:none', 'placeholder': 'Nhập gì đó...'}), label='Mô tả')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'description']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']