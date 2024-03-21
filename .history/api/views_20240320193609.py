from typing import Any
from django.http import HttpResponse
from rest_framework.views import View
from api.models import WeatherEntity
from datetime import datetime
from random import randrange
from django.shortcuts import render, redirect
from .repositories import WeatherRepository
from .serializers import WeatherSerializer

class WeatherView(View):
    
    serializer_class = WeatherSerializer
        
    def __init__(self, **kwargs: Any) -> None:
        self.repository = WeatherRepository(collectionName='weathers')

    def get(self, request):
        repository = WeatherRepository(collectionName='weathers')
        weathers = repository.get_all()
        serializer = self.serializer_class(weathers, many=True)
        serialized_weathers = serializer.serialize()
        return render(request, "home.html", {"weathers":serialized_weathers})


class WeatherGenerate(View):
    
    repository = ''
    serializer_class = WeatherSerializer

    
    def __init__(self, **kwargs: Any) -> None:
        self.repository = WeatherRepository(collectionName='weathers')
    
    def get(self, request):
        CIDADES_BRASIL = ["São Paulo", "Rio de Janeiro", "Salvador", "Brasília", "Fortaleza", "Belo Horizonte", "Manaus", "Curitiba", "Recife", "Porto Alegre"];
        CONDICOES_TEMPO = ["Ensolarado", "Nublado", "Chuvoso", "Neve", "Tempestade", "Parcialmente nublado", "Neblina", "Ventania"];
        now = datetime.now()
        now_formated = now.strftime("%d/%m/%Y %H:%M:%S")
        weather = {
            "temperature":randrange(start=5, stop=30),
            "date":f"{now_formated}",
            "atmosphericPressure":f"{randrange(start=800, stop=1500)} hPa",
            'humidity': f'{randrange(start=20, stop=90)}%',
            'city':f'{CIDADES_BRASIL[randrange(start=0, stop=len(CIDADES_BRASIL))]}',
            'weather':f'{CONDICOES_TEMPO[randrange(start=0, stop=len(CONDICOES_TEMPO))]}'
            }
        self.repository.insert(weather)
        
        return redirect('Weather View')
    
    
class WeatherClear(View):
    
    repository = ''
    
    
    def __init__(self, **kwargs: Any) -> None:
        self.repository = WeatherRepository(collectionName='weathers')
    
    def get(self, request):
        self.repository.drop_all()
        return redirect('Weather View')
