from django.contrib import admin
from django.urls import path
from api.views import WeatherView, WeatherGenerate, WeatherClear

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', WeatherView.as_view(), name='Weather View'),
    path('generate', WeatherGenerate.as_view(), name='Generate Weather'),
    path('clear', WeatherClear.as_view(), name='Clear Database')
]
