from django.contrib import admin
from django.urls import path
from api.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', WeatherView.as_view(), name='Weather View'),
    path('generate', WeatherGenerate.as_view(), name='Generate Weather'),
    path('insert', WeatherInsert.as_view(), name='Insert Weather'),
    path('clear', WeatherClear.as_view(), name='Clear Database'),
    path('edit/<str:id>', WeatherEdit.as_view(), name='Weather Edit'),
    path('remove/<str:id>', WeatherRemove.as_view(), name='Weather Remove'),
    path('filter', WeatherFilter.as_view(), name='Weather Filter')]
