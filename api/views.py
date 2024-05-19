from typing import Any
from django.http import HttpResponse
from rest_framework.views import View
from api.models import WeatherEntity
from datetime import datetime
from random import randrange
from django.shortcuts import render, redirect
from .repositories import WeatherRepository
from .serializers import WeatherSerializer
from .forms import WeatherForm
from .exceptions import WeatherException

MAIN_VIEW = 'Weather View'

class WeatherView(View):
    

        
    def __init__(self, **kwargs: Any) -> None:
        self.repository = WeatherRepository(collection_name='weathers')

    def get(self, request):
        try:
            repository = WeatherRepository(collection_name='weathers')
            weathers = list(repository.get_all())
            serializer = WeatherSerializer(data=weathers, many=True)
            if serializer.is_valid():
                weathers_data = serializer.data
                return render(request, "home.html", {"weathers": weathers_data})
            else:
                return render(request, "home.html", {"error": serializer.errors})
        except Exception as e:
            return render(request, "home.html", {"error": str(e)})
    
    def post(self, request):
        weather_data = {
            "temperature": request.POST.get("temperature"),
            "date": request.POST.get("date"),
            "atmospheric_pressure": request.POST.get("atmospheric_pressure"),
            "humidity": request.POST.get("humidity"),
            "city": request.POST.get("city"),
            "weather": request.POST.get("weather")
        }
        self.repository.insert(weather_data)
        
        return redirect(MAIN_VIEW)

    def put(self, request):
        weather_id = request.POST.get("weather_id")
        weather_data = {
            "temperature": request.POST.get("temperature"),
            "date": request.POST.get("date"),
            "atmospheric_pressure": request.POST.get("atmospheric_pressure"),
            "humidity": request.POST.get("humidity"),
            "city": request.POST.get("city"),
            "weather": request.POST.get("weather")
        }
        query = {"_id": weather_id}
        self.repository.update(query, weather_data)
        return redirect(MAIN_VIEW)

    def delete(self, request):
        weather_id = request.POST.get("weather_id")
        query = {"_id": weather_id}
        self.repository.delete(query)
        return redirect(MAIN_VIEW)


class WeatherGenerate(View):
    
    repository = ''

    
    def __init__(self, **kwargs: Any) -> None:
        self.repository = WeatherRepository(collection_name='weathers')
    
    def get(self, request):
        CIDADES_BRASIL = ["São Paulo", "Rio de Janeiro", "Salvador", "Brasília", "Fortaleza", "Belo Horizonte", "Manaus", "Curitiba", "Recife", "Porto Alegre"];
        CONDICOES_TEMPO = ["Ensolarado", "Nublado", "Chuvoso", "Neve", "Tempestade", "Parcialmente nublado", "Neblina", "Ventania"];
        weather_data = {
            "temperature": randrange(5, 30),
            "date": datetime.now(),
            "atmospheric_pressure": randrange(800, 1500),
            "humidity": randrange(20, 90),
            "city": CIDADES_BRASIL[randrange(len(CIDADES_BRASIL))],
            "weather": CONDICOES_TEMPO[randrange(len(CONDICOES_TEMPO))]
        }
        
        # Create an instance of the WeatherSerializer with weather_data
        serializer = WeatherSerializer(data=weather_data)
        
        if serializer.is_valid():
            # Save the new WeatherEntity object to the database using the repository
            self.repository.insert(serializer.validated_data)
        else:
            # If the data is invalid, print the errors to the console
            print(serializer.errors)

        # Redirect to the main weather view
        return redirect(MAIN_VIEW)

    
    
class WeatherClear(View):
    
    repository = ''
    
    
    def __init__(self, **kwargs: Any) -> None:
        self.repository = WeatherRepository(collection_name='weathers')
    
    def get(self, request):
        self.repository.drop_all()
        return redirect(MAIN_VIEW)


class WeatherInsert(View):
    
  
    repository = ''
    
    def __init__(self,) -> None:
        self.repository = WeatherRepository(collection_name='weathers')
        
    def get(self, request):
        weather_form = WeatherForm()
        weathers = list(self.repository.get_all())
        serializer = WeatherSerializer(data=weathers, many=True)
        if serializer.is_valid():
            weathers_data = serializer.data
        return render(request, "add_weather.html", {"form":weather_form, "weathers": weathers_data})
    
    def post(self, request):
        weather_form = WeatherForm(request.POST)
        if weather_form.is_valid():
            serializer = WeatherSerializer(data=weather_form.data)
            if (serializer.is_valid()):
                repository = WeatherRepository(collection_name='weathers')
                repository.insert(serializer.validated_data)
            else:
                print(serializer.errors)
        else:
            print(weather_form.errors)

        return redirect(MAIN_VIEW)
    
    
class WeatherEdit(View):
  
  repository = ''
  
  def __init__(self,) -> None:
    self.repository = WeatherRepository(collection_name='weathers')
  
  def post(self, request, id):
      weather_form = WeatherForm(request.POST)
      if weather_form.is_valid():
          serializer = WeatherSerializer(data=weather_form.data)
          if (serializer.is_valid()):
              repository = WeatherRepository(collection_name='weathers')
              repository.update(id, serializer.validated_data)
          else:
              print(serializer.errors)
      else:
          print(weather_form.errors)

      return redirect(MAIN_VIEW)
  
  def get(self, request, id):
      weather_data = self.repository.get_by_id(id)
      weather_form = WeatherForm(initial=weather_data)
      weathers = list(self.repository.get_all())
      serializer = WeatherSerializer(data=weathers, many=True)
      if serializer.is_valid():
        weathers_data = serializer.data
        return render(request, "edit_weather.html", {"form":weather_form, 'id':id, "weathers": weathers_data})

  
class WeatherRemove(View):
    
    repository = ''
    
    def __init__(self,) -> None:
        self.repository = WeatherRepository(collection_name='weathers')
    
    def get(self, request, id):
        self.repository.drop_by_id(id)
        return redirect(MAIN_VIEW)
    
    
    
class WeatherFilter(View):
    def post(self, request):
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')

        repository = WeatherRepository(collection_name='weathers')
        try:
            weathers = list(repository.get(data))
            serializer = WeatherSerializer(data=weathers, many=True)
            if (serializer.is_valid()):

                model_weather = serializer.save()
                object_return = {"weathers":model_weather}
            else:

                object_return = {"error":serializer.errors}
        except WeatherException as e:
            object_return = {"error":e.message}
  
        return render(request, "home.html", object_return)