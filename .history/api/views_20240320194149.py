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
    main_view = 'Weather View'
        
    def __init__(self, **kwargs: Any) -> None:
        self.repository = WeatherRepository(collection_name='weathers')

    def get(self, request):
        weathers = self.repository.get_all()
        serializer = self.serializer_class(weathers, many=True)
        serialized_weathers = serializer.serialize()
        return render(request, "home.html", {"weathers":serialized_weathers})
    
    def post(self, request):
        weather_data = {
            "temperature": request.POST.get("temperature"),
            "date": request.POST.get("date"),
            "atmosphericPressure": request.POST.get("atmosphericPressure"),
            "humidity": request.POST.get("humidity"),
            "city": request.POST.get("city"),
            "weather": request.POST.get("weather")
        }
        self.repository.insert(weather_data)
        
        return redirect(self.main_view)

    def put(self, request):
        weather_id = request.POST.get("weather_id")
        weather_data = {
            "temperature": request.POST.get("temperature"),
            "date": request.POST.get("date"),
            "atmosphericPressure": request.POST.get("atmosphericPressure"),
            "humidity": request.POST.get("humidity"),
            "city": request.POST.get("city"),
            "weather": request.POST.get("weather")
        }
        query = {"_id": weather_id}
        self.repository.update(query, weather_data)
        return redirect(self.main_view)

    def delete(self, request):
        weather_id = request.POST.get("weather_id")
        query = {"_id": weather_id}
        self.repository.delete(query)
        return redirect('Weather View')


class WeatherGenerate(View):
    
    repository = ''
    serializer_class = WeatherSerializer

    
    def __init__(self, **kwargs: Any) -> None:
        self.repository = WeatherRepository(collection_name='weathers')
    
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
        self.repository = WeatherRepository(collection_name='weathers')
    
    def get(self, request):
        self.repository.drop_all()
        return redirect('Weather View')
