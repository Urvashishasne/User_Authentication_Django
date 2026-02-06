from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Only letters/numbers, 3-20 characters
        if not re.match("^[A-Za-z0-9]{3,20}$", username):
            raise ValidationError("Username must be 3-20 characters and contain only letters or numbers")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already taken")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Passwords do not match")
