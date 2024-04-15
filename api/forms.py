from django import forms
from .models import WeatherEntity

class WeatherForm(forms.Form):
    temperature = forms.FloatField()
    date = forms.DateTimeField()
    city = forms.CharField(max_length=255)
    atmospheric_pressure = forms.FloatField()
    humidity =  forms.FloatField()
    weather = forms.CharField(max_length=255)
    
    
