from django.contrib import admin
from django.urls import path
from api.views import WeatherView, AboutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', WeatherView.as_view()),
    path('about', AboutView.as_view())
]
