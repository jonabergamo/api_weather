from django.http import HttpResponse
from rest_framework.views import View
from api.models import WeatherEntity
from datetime import datetime
from random import randrange
from django.shortcuts import render

class WeatherView(View):
    

    def get(self, request):
        weathers = []
        for i in range(10):
            weathers.append(WeatherEntity(
            temperature=randrange(25, 35),
            city='Sorocaba',
            atmosphericPressure='Razoavel',
            humidity='Seco', weather='Chuvoso',
            date=datetime.now))
        # return HttpResponse(weathers)
        
        return render(request, "home.html", {"weathers": weathers})
