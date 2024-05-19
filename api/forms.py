from django import forms
from .models import WeatherEntity
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class WeatherForm(forms.Form):
    temperature = forms.FloatField()
    date = forms.DateTimeField()
    city = forms.CharField(max_length=255)
    atmospheric_pressure = forms.FloatField()
    humidity =  forms.FloatField()
    weather = forms.CharField(max_length=255)
    
    
class LoginForm(forms.Form):
    email = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
