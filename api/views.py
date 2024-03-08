from django.http import HttpResponse
from rest_framework.views import View
from api.models import WeatherEntity
from datetime import datetime
from random import randrange
from django.shortcuts import render, redirect
from .repositories import WeatherRepository

class WeatherView(View):
    def get(self, request):
        repository = WeatherRepository(collectionName='weathers')
        weathers = repository.getAll()
        return render(request, "home.html", {"weathers":weathers})


class WeatherGenerate(View):
    
    def get(self, request):
        repository = WeatherRepository(collectionName='weathers')
        # weather = WeatherEntity(temperature=randrange(start=1, step=23), date=datetime.now())
        weather = {
            "temperature":25,
            "date":f"{datetime.now()}"
            }
        repository.insert(weather)
        
        return redirect('Weather View')
    
    
class WeatherClear(View):
    
    def get(self, request):
        repository = WeatherRepository(collectionName='weathers')
        repository.dropAll()
        return redirect('Weather View')
