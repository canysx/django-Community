from django import forms

from .models import UserProfile, Topic


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=5)


class WriteForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['image', 'title', 'content']
