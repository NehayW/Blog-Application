from django.shortcuts import redirect, render
from django.views import View
from .models import *
from django.contrib import messages
# Create your views here.


class ChatUser(View):
    def get(self, request):
        user_rooms = ChatRoom.objects.filter(room=request.user)
        return render(request, "room.html" ,{"user_rooms": user_rooms})
