from django.urls import path
from .views import *


urlpatterns = [
    path('room/', ChatUser.as_view(), name="room"),
]
