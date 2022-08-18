from django.shortcuts import redirect, render
from django.views import View
from .models import *
from django.contrib import messages
# Create your views here.


class ChatUser(View):
    def get(self, request):
        if request.user.is_authenticated:
            user_rooms = ChatRoom.objects.filter(room=request.user)
            return render(request, "room.html" ,{"user_rooms": user_rooms})
            
        else:
            return redirect("login")
# class AllRooms(View):
#     def get(self,request):
#         rooms=ChatRoom.objects.all()
#         serializer=AllRoomSerializer(rooms, many=True)
#         return Response({"data":serializer.data})           

# class PersonalRooms(View):
#     def get(self, request):
#         my_room = ChatRoom.objects.filter(room=request.user)
#         serializer=AllRoomSerializer(my_room, many=True)
#         return Response({"data":serializer.data})

# class MyChat(View):
#     def get(self, request, room):
#         message=Message.objects.filter(room_name=room)
#         message=self.paginate_queryset(message, request, view=True)
#         serializer=MessageSerializer(message, many=True)
#         return self.get_paginated_response({"user":request.user.id, "data": serializer.data})