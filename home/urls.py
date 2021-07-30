from django.urls import path
from home.views import *
app_name = "home"

urlpatterns = [
    path('', index, name="home"),
    path('seed', seed, name="seed"),
]