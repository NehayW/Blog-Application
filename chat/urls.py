from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('room/', login_required(ChatUser.as_view()), name="room"),
]
