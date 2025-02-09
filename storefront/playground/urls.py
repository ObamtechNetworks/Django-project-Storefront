# path function from the url package
from django.urls import path
from . import views

# URL CONFIGURATION
urlpatterns = [
    path('hello/', views.say_hello)
]
