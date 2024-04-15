from django.contrib import admin
from django.urls import path
from api.views import WeatherView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', WeatherView.as_view())
]
