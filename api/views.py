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
        cidadesBrasil = ["São Paulo", "Rio de Janeiro", "Salvador", "Brasília", "Fortaleza", "Belo Horizonte", "Manaus", "Curitiba", "Recife", "Porto Alegre"];
        condicoesTempo = ["Ensolarado", "Nublado", "Chuvoso", "Neve", "Tempestade", "Parcialmente nublado", "Neblina", "Ventania"];
        now = datetime.now()
        now_formated = now.strftime("%d/%m/%Y %H:%M:%S")
        weather = {
            "temperature":randrange(start=5, stop=30),
            "date":f"{now_formated}",
            "atmosphericPressure":f"{randrange(start=800, stop=1500)} hPa",
            'humidity': f'{randrange(start=20, stop=90)}%',
            'city':f'{cidadesBrasil[randrange(start=0, stop=len(cidadesBrasil))]}',
            'weather':f'{condicoesTempo[randrange(start=0, stop=len(condicoesTempo))]}'
            }
        repository.insert(weather)
        
        return redirect('Weather View')
    
    
class WeatherClear(View):
    
    def get(self, request):
        repository = WeatherRepository(collectionName='weathers')
        repository.dropAll()
        return redirect('Weather View')
