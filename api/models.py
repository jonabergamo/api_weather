from typing import Any
from django.db import models

class WeatherEntity:
    
    def __init__(self, temperature, city, atmospheric_pressure, humidity, weather, date, id=None) -> None:
        self.id = id
        self.temperature = temperature
        self.city = city
        self.atmospheric_pressure = atmospheric_pressure
        self.humidity = humidity
        self.weather = weather
        self.date = date

        
    def __str__(self) -> str:
        return (f"Weather <{self.temperature}>")
    
    def __getattribute__(self, __name: str) -> Any:
        if (__name=='date'):
            return object.__getattribute__(self, __name).strftime("%d/%m/%Y %H:%M:%S")
        else:
            return object.__getattribute__(self, __name)
