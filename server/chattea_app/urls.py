from django.urls import path 
from . import views

urlpatterns = [
    path("chattea/", views.index, name="index"),
]
